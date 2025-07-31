from pathlib import Path
import re

def hex_to_rgb(hex_color: str) -> str:
    hex_color = hex_color.lstrip('#')
    return ','.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

def load_color_variables_from_scss(scss_path: Path) -> dict:
    variables = {}
    pattern = re.compile(r"(\w+):\s*(#[0-9a-fA-F]{6});")
    content = scss_path.read_text(encoding="utf-8")
    for name, hexcolor in pattern.findall(content):
        variables[name] = hex_to_rgb(hexcolor)
    return variables

def compile_qss_with_variables(qss_text: str, variables: dict) -> str:
    def repl(m):
        var_name = m.group(1).strip()
        if var_name.endswith('.rgb'):
            var_name = var_name[:-4]
        rgb = variables.get(var_name)
        if not rgb:
            return "0,0,0"
        return rgb
    return re.sub(r"rgb\s*\(\s*<([^>]+)>\s*\)", lambda m: f"rgb({repl(m)})", qss_text)

def compile_all_qss(qss_dir: Path, scss_path: Path = None) -> dict:
    variables = load_color_variables_from_scss(scss_path) if scss_path and scss_path.exists() else {}
    compiled_parts = {}

    for qss_file in sorted(qss_dir.glob("*.qss")):
        name = qss_file.stem
        content = qss_file.read_text(encoding="utf-8")
        compiled = compile_qss_with_variables(content, variables) if variables else content
        compiled_parts[name] = compiled

    return compiled_parts

def cache_compiled_qss(
    qss_dir: Path = Path.home() / ".config/Modus/styles",
    scss_path: Path = Path.home() / ".cache/material/colors.scss",
    cache_dir: Path = Path.home() / ".cache/material/cached_colors"
) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    compiled_parts = compile_all_qss(qss_dir, scss_path)

    for name, content in compiled_parts.items():
        cache_file = cache_dir / f"{name}.compiled.qss"
        cache_file.write_text(content, encoding="utf-8")

    return compiled_parts

def load_compiled_qss(
    name: str,
    cache_dir: Path = Path.home() / ".cache/material/cached_colors"
) -> str:
    cache_file = cache_dir / f"{name}.compiled.qss"
    if not cache_file.exists():
        raise FileNotFoundError(f"Cache file not found for '{name}': {cache_file}")
    return cache_file.read_text(encoding="utf-8")

if __name__ == "__main__":
    qss_dir = Path.home() / ".config/Modus/styles"
    scss_path = Path.home() / ".cache/material/colors.scss"
    cache_dir = Path.home() / ".cache/material/cached_colors"

    print("Compiling and caching QSS...")
    cache_compiled_qss(qss_dir, scss_path, cache_dir)

    try:
        qss_text = load_compiled_qss("config", cache_dir)
        print(f"Loaded 'config' QSS, length: {len(qss_text)}")
    except FileNotFoundError as e:
        print(str(e))
