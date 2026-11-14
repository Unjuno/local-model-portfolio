"""Offline tests: fail closed on unsafe HTTP ranges and malformed tensor headers."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'scripts' / 'safetensors_header_census.py'
if MODULE.exists():
    spec = importlib.util.spec_from_file_location('header_census', MODULE)
    census = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(census)
else:
    census = None


def encode(value):
    return json.dumps(value, separators=(',', ':')).encode()


class FakeResponse:
    def __init__(self, status=206, content_range='bytes 0-7/100', body=b'12345678'):
        self.status = status
        self.headers = {'Content-Range': content_range, 'Content-Length': str(len(body))}
        self.body, self.reads, self.closed = body, [], False
    def read(self, count):
        self.reads.append(count)
        result, self.body = self.body[:count], self.body[count:]
        return result
    def close(self):
        self.closed = True


class ModuleExists(unittest.TestCase):
    def test_implementation_exists(self):
        self.assertIsNotNone(census, 'Header-only census implementation is required')


@unittest.skipIf(census is None, 'Implementation not yet present')
class HeaderCensus(unittest.TestCase):
    def test_valid_mixed_dtypes_and_scalar(self):
        obj = {'__metadata__': {'format': 'pt'},
               'w': {'dtype': 'BF16', 'shape': [2, 3], 'data_offsets': [0, 12]},
               'scale': {'dtype': 'F32', 'shape': [], 'data_offsets': [12, 16]}}
        result = census.inspect_header(encode(obj), 16)
        self.assertEqual(result['stored_elements'], 7)
        self.assertEqual(result['tensor_count'], 2)
        self.assertEqual(result['dtype_elements'], {'BF16': 6, 'F32': 1})

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):
            census.inspect_header(b'{"x":{},"x":{}}', 0)

    def test_non_contiguous_offsets_rejected(self):
        cases = [
            {'a': {'dtype':'F32','shape':[1],'data_offsets':[1,5]}},
            {'a': {'dtype':'F32','shape':[1],'data_offsets':[0,4]},
             'b': {'dtype':'F32','shape':[1],'data_offsets':[2,6]}},
            {'a': {'dtype':'F32','shape':[1],'data_offsets':[0,4]}}]
        for obj in cases:
            with self.subTest(obj=obj), self.assertRaises(ValueError):
                census.inspect_header(encode(obj), 8)

    def test_packed_and_unknown_dtype_rejected(self):
        for dtype in ['I4', 'NVFP4', 'UNKNOWN']:
            with self.subTest(dtype=dtype), self.assertRaises(ValueError):
                census.inspect_header(encode({'a':{'dtype':dtype,'shape':[2],
                                                   'data_offsets':[0,1]}}), 1)

    def test_invalid_dimensions_and_offsets_rejected(self):
        for shape in [[True], [-1], [1.5], [2**64], '2']:
            with self.subTest(shape=shape), self.assertRaises(ValueError):
                census.inspect_header(encode({'a':{'dtype':'F32','shape':shape,
                                                   'data_offsets':[0,4]}}), 4)
        with self.assertRaises(ValueError):
            census.inspect_header(encode({'a':{'dtype':'F32','shape':[1],
                                               'data_offsets':[False,4]}}), 4)

    def test_empty_tensor_and_scalar_allowed(self):
        obj={'empty':{'dtype':'F32','shape':[0],'data_offsets':[0,0]},
             'scalar':{'dtype':'F32','shape':[],'data_offsets':[0,4]}}
        self.assertEqual(census.inspect_header(encode(obj),4)['stored_elements'],1)

    def test_200_response_rejected_before_body_read(self):
        response = FakeResponse(status=200)
        with self.assertRaises(ValueError):
            census.read_exact_range(response, 0, 7, 100)
        self.assertEqual(response.reads, [])
        self.assertTrue(response.closed)

    def test_wrong_range_or_length_rejected_without_read(self):
        for response in [FakeResponse(content_range='bytes 0-15/100'),
                         FakeResponse(content_range='bytes 0-7/101'),
                         FakeResponse(body=b'123456789')]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                census.read_exact_range(response,0,7,100)
            self.assertEqual(response.reads,[])
            self.assertTrue(response.closed)

    def test_correct_range_and_short_body(self):
        response=FakeResponse()
        self.assertEqual(census.read_exact_range(response,0,7,100), b'12345678')
        self.assertEqual(response.reads,[8])
        response=FakeResponse(body=b'12')
        response.headers['Content-Length']='8'
        with self.assertRaises(ValueError):
            census.read_exact_range(response,0,7,100)

    def test_component_prefix_disambiguates_tensor_names(self):
        report={'stored_elements':3,'tensor_count':1,'tensor_names':['w'],
                'dtype_elements':{'BF16':3}}
        rows=[{'component':'a','file':'a/1','summary':report},
              {'component':'b','file':'b/1','summary':report}]
        self.assertEqual(census.aggregate(rows)['stored_elements_upper_bound'],6)
        rows[1]['component']='a'
        with self.assertRaises(ValueError):
            census.aggregate(rows)

    def test_http_redirect_and_path_guard(self):
        self.assertTrue(census.allowed_url('https://huggingface.co/a/b'))
        self.assertTrue(census.allowed_url('https://cas-bridge.xethub.hf.co/x'))
        for url in ['http://huggingface.co/x','https://evil-hf.co/x',
                    'https://huggingface.co.evil.test/x','https://user:pw@huggingface.co/x']:
            self.assertFalse(census.allowed_url(url))
        for path in ['../model.safetensors','/model.safetensors','a/../model.safetensors']:
            with self.assertRaises(ValueError):
                census.validate_file_path(path)


if __name__ == '__main__':
    unittest.main()
