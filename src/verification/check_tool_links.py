"""Live link-check for every entry in the manuscript's tool inventory (Table 4).

Checks each repository URL cited in `manuscript/manuscript.tex`'s
`table:tools-from-corpus` for HTTP resolvability, and where the platform's
API exposes one, the resolved commit SHA. Writes a timestamped log to
`src/verification/output/tool_link_check.log` as a supplementary,
independently reproducible verification artefact.

HuggingFace model/dataset pages return HTTP 401 to an unauthenticated HEAD
request even when the resource is public; this script treats a successful
HuggingFace API lookup (which does not require auth for public resources)
as the authoritative check for `huggingface.co` URLs, and a plain HTTP GET
status for everything else.

Usage:
    python -m src.verification.check_tool_links
"""

import datetime
import json
import urllib.error
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
LOG_PATH = OUTPUT_DIR / "tool_link_check.txt"

# (Paper, Tool name, canonical URL) for every row in table:tools-from-corpus,
# including the two provenance-track additions.
TOOL_LINKS = [
    ("P001", "MoVoC-Tok", "https://huggingface.co/spaces/Hailay/movoc-tok-playground"),
    ("P003", "amharic-ir-benchmarks", "https://github.com/kidist-amde/amharic-ir-benchmarks"),
    ("P003", "roberta-amharic-text-embedding-base", "https://huggingface.co/rasyosef/roberta-amharic-text-embedding-base"),
    ("P003", "roberta-amharic-text-embedding-medium", "https://huggingface.co/rasyosef/roberta-amharic-text-embedding-medium"),
    ("P003", "ColBERT-Mini (Amharic)", "https://huggingface.co/rasyosef/ColBERT-Mini"),
    ("P006", "Ethiobenchmark task datasets (EthioPOS)", "https://huggingface.co/datasets/EthioNLP/EthioPOS"),
    ("P006", "EthioLLM model family", "https://huggingface.co/EthioNLP/EthioLLM-l-250K"),
    ("P011", "Amharic sentiment dataset", "https://github.com/uhh-lt/ASAB"),
    ("P013", "amseg", "https://github.com/uhh-lt/amharicprocessor"),
    ("P015", "Tigrinya NER dataset", "https://github.com/mehari-eng/Tigrinya-NER"),
    ("P016", "GeezSwitch", "https://github.com/fgaim/geezswitch"),
    ("P016", "GeezSwitch-data", "https://github.com/fgaim/GeezSwitch-data"),
    ("P017", "Amharic UD Treebank", "https://github.com/UniversalDependencies/UD_Amharic-ATT"),
    ("P019", "AmQA (GitHub)", "https://github.com/semantic-systems/amharic-qa"),
    ("P019", "AmQA (HF)", "https://huggingface.co/datasets/dagim/amharic-qa"),
    ("P020", "EthioProverbEval", "https://github.com/EthioNLP/EthioProverbEval"),
    ("P020", "ProverbEval benchmark", "https://huggingface.co/datasets/israel/ProverbEval"),
    ("P026", "TiALD", "https://github.com/fgaim/TiALD"),
    ("P026", "TiALD dataset", "https://huggingface.co/datasets/fgaim/tigrinya-abusive-language-detection"),
    ("P029", "TLMD", "https://zenodo.org/records/5139094"),
    ("P030", "Tigrinya PLMs (TiBERT)", "https://huggingface.co/fgaim/tibert-base"),
    ("P030", "Tigrinya PLMs (TiRoBERTa)", "https://huggingface.co/fgaim/tiroberta-base"),
    ("P030", "Tigrinya PLMs (TiELECTRA)", "https://huggingface.co/fgaim/tielectra-small"),
    ("P031", "Walia-LLM", "https://huggingface.co/israel/LLAMA-Walia-II"),
    ("P035", "2AIRTC", "https://huggingface.co/datasets/rasyosef/2AIRTC-Amharic-Adhoc-Information-Retrieval-Test-Collection"),
    ("P041", "EthioEmo-intensities (GitHub)", "https://github.com/Tadesse-Destaw/EthioEmo"),
    ("P041", "EthioEmo-intensities (HF)", "https://huggingface.co/datasets/Tadesse/EthioEmo-intensities"),
    ("P081", "ASED", "https://github.com/Ethio2021/ASED_V1"),
    ("P084", "amharic_word_embeddings", "https://github.com/leobitz/amharic_word_embeddings"),
    ("N/A (provenance-track)", "HornMorpho", "https://github.com/hltdi/HornMorpho"),
    ("N/A (provenance-track)", "MasakhaNER 1.0", "https://github.com/masakhane-io/masakhane-ner"),
]


def _github_sha(owner_repo: str) -> str:
    url = f"https://api.github.com/repos/{owner_repo}/commits?per_page=1"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)
    return data[0]["sha"][:12] if data else "unknown"


def _check_one(paper: str, name: str, url: str) -> str:
    access_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    try:
        if "github.com" in url:
            owner_repo = url.split("github.com/", 1)[1].rstrip("/")
            owner_repo = "/".join(owner_repo.split("/")[:2])
            try:
                sha = _github_sha(owner_repo)
                status = "OK (200, via GitHub API)"
            except urllib.error.HTTPError as e:
                if e.code in (403, 429):
                    # Unauthenticated GitHub API rate limit (60 req/hour) -- fall back
                    # to a plain page fetch, which is not rate-limited the same way.
                    req = urllib.request.Request(url, method="HEAD")
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        pass
                    sha = "n/a (rate-limited)"
                    status = "OK (200, API rate-limited)"
                else:
                    raise
            return f"{paper:24} {name:42} {status:26} sha={sha:14} {access_date}  {url}"
        elif "huggingface.co" in url:
            # Public HF resources 401 on unauthenticated HEAD but resolve via the API.
            if "/datasets/" in url:
                slug = url.split("/datasets/", 1)[1]
                api = f"https://huggingface.co/api/datasets/{slug}"
            elif "/spaces/" in url:
                slug = url.split("/spaces/", 1)[1]
                api = f"https://huggingface.co/api/spaces/{slug}"
            else:
                slug = url.rstrip("/").split("huggingface.co/", 1)[1]
                api = f"https://huggingface.co/api/models/{slug}"
            with urllib.request.urlopen(api, timeout=15) as resp:
                data = json.load(resp)
            sha = (data.get("sha") or "unknown")[:12]
            status = "OK (200, via HF API)"
            return f"{paper:24} {name:42} {status:26} sha={sha:14} {access_date}  {url}"
        else:
            last_error: Exception = RuntimeError("unreachable")
            for attempt_timeout in (15, 30):
                try:
                    req = urllib.request.Request(url, method="HEAD")
                    with urllib.request.urlopen(req, timeout=attempt_timeout) as resp:
                        status = f"OK ({resp.status})"
                    return f"{paper:24} {name:42} {status:26} sha={'n/a':14} {access_date}  {url}"
                except (TimeoutError, urllib.error.URLError) as e:
                    last_error = e
            raise last_error
    except urllib.error.HTTPError as e:
        return f"{paper:24} {name:42} {'FAIL (' + str(e.code) + ')':26} sha={'n/a':14} {access_date}  {url}"
    except Exception as e:  # noqa: BLE001 -- this is a diagnostic script, report and continue
        return f"{paper:24} {name:42} {'FAIL (' + type(e).__name__ + ')':26} sha={'n/a':14} {access_date}  {url}"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        f"Tool-inventory link check -- {len(TOOL_LINKS)} entries "
        f"(Table 4, manuscript/manuscript.tex) -- generated {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        "=" * 100,
    ]
    fail_count = 0
    for paper, name, url in TOOL_LINKS:
        result = _check_one(paper, name, url)
        lines.append(result)
        if "FAIL" in result:
            fail_count += 1
    lines.append("=" * 100)
    lines.append(f"{len(TOOL_LINKS) - fail_count}/{len(TOOL_LINKS)} links resolved successfully.")

    LOG_PATH.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nLog written to {LOG_PATH}")


if __name__ == "__main__":
    main()
