# Static Site Generator

This is a custom-built Static Site Generator (SSG) written in Python. It transforms raw Markdown files and static assets into a structured HTML website using a recursive build process.

## How It Works

The generator follows a specific build pipeline:
1. **Directory Management**: It ensures the output directory is prepared for a fresh build of the site.
2. **Asset Synchronization**: It recursively copies all files from the `static` folder (images, CSS, etc.) to the output destination.
3. **Content Transformation**: It crawls the `content` directory for `.md` files, converts them into HTML nodes, and injects the resulting HTML into a `template.html` file.
4. **Structure Preservation**: The generator mirrors the nested directory structure of your `content` folder in the final build.

## Key Components

### 1. HTMLNode Tree
The project uses a recursive `HTMLNode` class (and its subclasses `LeafNode` and `ParentNode`). This allows the generator to represent complex, nested HTML structures in a way that Python can easily manipulate and render.

### 2. Block-Based Markdown Parser
The parser identifies different Markdown blocks (headers, code, quotes, lists, and paragraphs) and handles inline styling like **bold**, *italic*, and `code` spans.

### 3. Recursive Page Generation
The `generate_pages_recursive` function walks through the entire `content` directory, ensuring that every Markdown file—no matter how deep the nesting—is found and converted.

## Getting Started

### Prerequisites
- Python 3.x installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

### Installation
1. Add your Markdown content to the content/ directory.
2. Place your CSS and images in the static/ directory.
3. Ensure your template.html contains the {{ Title }} and {{ Content }} placeholders.
4. Run the generator:
    ```bash
    ./main.sh
    ```
5. Your generated site is now ready in the output directory!