import hashlib
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from chapter_qa.adversary import make_identity
from chapter_qa.render_completeness import emit_render_evidence
ROOT = Path(".").resolve()
relative = "qa/work/_v12/p1-versio.png"
path = ROOT / relative
path.parent.mkdir(parents=True, exist_ok=True)
data = b"\x89PNG\r\nversion"
path.write_bytes(data)
identity = make_identity()
row = {
    "artifactId": "notes", "artifactHash": "b" * 64, "pageOrSlide": 1,
    "renderPath": relative, "renderHash": hashlib.sha256(data).hexdigest(),
    "navigation": False, "buildId": identity.buildId,
}
stored, result = emit_render_evidence([row], [row], identity, row["renderPath"])
print(result.status, result.reasons)
print(stored["findings"])
print(stored["failureReason"])
print(stored["execution"])
