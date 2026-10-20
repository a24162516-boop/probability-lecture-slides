"""Windows 인증서 저장소(ROOT, CA)를 PEM 파일로 내보내기.

사용: python -I make_ca_bundle.py 출력경로.pem
pip install --cert 출력경로.pem ... 또는 ssl.create_default_context(cafile=...) 에 사용.
"""
import ssl
import sys
from pathlib import Path

out = Path(sys.argv[1] if len(sys.argv) > 1 else "winca.pem")
out.parent.mkdir(parents=True, exist_ok=True)
pems = [ssl.DER_cert_to_PEM_cert(cert)
        for store in ("ROOT", "CA")
        for cert, enc, _ in ssl.enum_certificates(store) if enc == "x509_asn"]
out.write_text("".join(pems))
print(f"{len(pems)} certs -> {out}")
