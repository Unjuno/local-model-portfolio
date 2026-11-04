"""Offline v12 tests; standard library only; no downloads or model execution."""
import unittest
from scripts.check_parameter_cutoff import audit, validate_model, verified_quant_exception, LOW, UNKNOWN, REVIEW, VERIFIED

CAP = 150_000_000_000


def record(n, status, decision="select", tier="R1"):
    return {"repo_id":"unit/model","asset_kind":"model","risk_tier":tier,
            "portfolio_decision":decision,"parameter_gate":{"total_parameters":n,"status":status}}


def verified_example():
    x=record(180_000_000_000,VERIFIED)
    x["quantized_exception"]={
        "status":"VERIFIED","quantized_repo_id":"unit/model-Q4-GGUF",
        "source_url":"https://huggingface.co/unit/model-Q4-GGUF",
        "source_revision_sha":"a"*40,"quantization_variant":"Q4",
        "backend_and_version":"llama.cpp commit aaaa",
        "hardware_record":"test 512GB RAM 24GB VRAM, actual available tracked",
        "total_model_parameters":180_000_000_000,
        "complete_selected_file_bytes":110_000_000_000,
        "measured_peak_host_ram_plus_vram_bytes":160_000_000_000,
        "context_tokens":8192,"batch_size":1,"throughput_trials":30,
        "independent_quality_n":30,"throughput_median_tokens_per_second":8.0,
        "minimum_acceptable_tokens_per_second":5.0,"measured_user_hardware":True,
        "task_quality_pass":True,"license_text_reviewed":True,
        "dependencies_reviewed":True,"personal_gated_access_verified":True,
    }
    return x


class ParameterBaselineTests(unittest.TestCase):
    def test_80b_normal(self):
        self.assertEqual([],validate_model(record(80_000_000_000,LOW)))
    def test_150b_and_180b_hold_allowed(self):
        for n in (150_000_000_000,180_000_000_000,1_050_000_000_000):
            self.assertEqual([],validate_model(record(n,REVIEW,"hold","HOLD")))
    def test_oversized_no_auto_adoption(self):
        self.assertTrue(validate_model(record(180_000_000_000,REVIEW)))
        self.assertTrue(validate_model(record(180_000_000_000,LOW)))
    def test_unknown_total_hold_only(self):
        self.assertEqual([],validate_model(record(None,UNKNOWN,"hold","HOLD")))
        self.assertTrue(validate_model(record(None,UNKNOWN)))
    def test_quantized_verified_valid(self):
        self.assertTrue(verified_quant_exception(verified_example()))
        self.assertEqual([],validate_model(verified_example()))
    def test_quantized_forged_shortcuts_fail(self):
        x=verified_example()
        x["quantized_exception"]["measured_peak_host_ram_plus_vram_bytes"]=512_000_000_000
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["throughput_trials"]=3
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["license_text_reviewed"]=False
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["total_model_parameters"]=6_000_000_000
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["task_quality_pass"]=False
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["source_revision_sha"]="main"
        self.assertTrue(validate_model(x))
        x=verified_example()
        x["quantized_exception"]["throughput_median_tokens_per_second"]=1.0
        self.assertTrue(validate_model(x))
    def test_current_repository(self):
        self.assertEqual([],audit())


if __name__=="__main__":
    unittest.main()
