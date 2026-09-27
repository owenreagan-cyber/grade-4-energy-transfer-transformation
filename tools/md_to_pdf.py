"""Render markdown (with tables) to PDF via markdown->HTML->LibreOffice."""
import sys, os, subprocess, tempfile
import markdown

CSS = """
<style>
body { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 11pt; line-height: 1.4;
       max-width: 900px; margin: 24px auto; color: #1a1a1a; }
h1 { color: #1F3A5F; font-size: 20pt; border-bottom: 2px solid #2E6E8E; padding-bottom: 6px; }
h2 { color: #2E6E8E; font-size: 15pt; margin-top: 20px; }
h3 { color: #1F3A5F; font-size: 12.5pt; margin-top: 16px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }
th, td { border: 1px solid #999; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #1F3A5F; color: #fff; }
tr:nth-child(even) td { background: #F3F6FA; }
code { background: #f0f0f0; padding: 0 3px; border-radius: 3px; }
blockquote { color: #555; border-left: 4px solid #2E6E8E; margin: 8px 0; padding-left: 12px; }
hr { border: none; border-top: 1px solid #ccc; margin: 18px 0; }
</style>
"""

def main():
    md_path = sys.argv[1]
    out_pdf = sys.argv[2]
    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'sane_lists'])
    html = f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{html}</body></html>"
    tmp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8')
    tmp.write(html); tmp.close()
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir',
                    os.path.dirname(os.path.abspath(out_pdf)), tmp.name],
                   check=True, capture_output=True)
    produced = os.path.join(os.path.dirname(os.path.abspath(out_pdf)),
                            os.path.splitext(os.path.basename(tmp.name))[0] + '.pdf')
    if os.path.abspath(produced) != os.path.abspath(out_pdf):
        os.replace(produced, out_pdf)
    os.unlink(tmp.name)
    print("wrote", out_pdf)

if __name__ == "__main__":
    main()
