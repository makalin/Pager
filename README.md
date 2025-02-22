# Pager - Minimalist Static Site Generator

Pager is a super-lightweight static site generator that transforms Markdown files into HTML sites with zero external dependencies (using only Python's standard library). It features custom Markdown codes, multiple themes including a unique retro CRT option, and simple configuration.

## Features

- **Zero Dependencies**: Pure Python implementation
- **Custom Markdown Codes**:
  - `:::animate:[fade|bounce|pulse] content :::` for CSS animations
  - `:::js:[alert|prompt] message :::` for interactive buttons
- **Themes**:
  - `default`: Clean and simple
  - `crt`: Retro CRT with scanlines and flicker
  - `dark`: Modern dark mode
- **Navigation**: Auto-generated nav bar
- **Configurable**: Via `config.json`
- **JavaScript Support**: Optional CDN library inclusion
- **Fast**: Built with Python for efficiency

## Installation

1. Clone the repository:
```bash
git clone https://github.com/makalin/pager.git
cd pager
```

2. Ensure Python 3.6+ is installed:
```bash
python3 --version
```

## Usage

1. Create a `content/` directory with Markdown files
2. (Optional) Create a `config.json`
3. Run Pager:
```bash
python3 pager.py
```

Output will be generated in the `public/` directory.

### Example Markdown (`content/index.md`)
```markdown
# Home

Welcome to my **bold** site with a [link](about.html).

:::animate:fade
This text fades in!
:::

:::js:alert Hello World
Click for an alert
:::
```

### Example Config (`config.json`)
```json
{
    "input_dir": "content",
    "output_dir": "public",
    "theme": "dark",
    "title": "My Cool Site",
    "javascript_libs": [
        "https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"
    ]
}
```

## Directory Structure
```
pager/
├── content/        # Markdown source files
├── public/        # Generated HTML output
├── config.json    # Configuration (optional)
└── pager.py       # Main script
```

## Custom Markdown Codes

- **Animations**:
  - `:::animate:fade content :::` - Fade in effect
  - `:::animate:bounce content :::` - Bouncing effect
  - `:::animate:pulse content :::` - Pulsing effect

- **JavaScript**:
  - `:::js:alert message :::` - Creates an alert button
  - `:::js:prompt message :::` - Creates a prompt button

## Themes

- **Default**: Minimal, clean design
- **CRT**: Retro terminal aesthetic with scanlines
- **Dark**: Sleek dark mode

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details
