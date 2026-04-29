# amre-assets

Image and artifact repository for **AMRE** — stores images, HTML files, and generated assets accessible via raw GitHub URLs.

## Structure

```
amre-assets/
├── images/      # PNG, JPG, SVG, GIF assets
├── html/        # HTML pages and generated artifacts
└── artifacts/   # PDFs, JSON, exports, misc files
```

## Accessing files

All files in this repository are accessible via raw URLs without authentication.

**Raw URL pattern:**

```
https://raw.githubusercontent.com/Hilex2030/amre-assets/main/<folder>/<filename>
```

**Examples:**

- Image: `https://raw.githubusercontent.com/Hilex2030/amre-assets/main/images/logo.png`
- - HTML: `https://raw.githubusercontent.com/Hilex2030/amre-assets/main/html/page.html`
  - - Artifact: `https://raw.githubusercontent.com/Hilex2030/amre-assets/main/artifacts/data.json`
   
    - ## Uploading files
   
    - **Via GitHub web UI:** navigate to the target folder, click `Add file → Upload files`, drag & drop, then commit.
   
    - **Via git:**
   
    - ```bash
      git clone https://github.com/Hilex2030/amre-assets.git
      cd amre-assets
      cp ~/path/to/file.png images/
      git add images/file.png
      git commit -m "Add file.png"
      git push
      ```

      ## Using with Claude

      Share a raw URL with Claude in any chat and Claude can fetch the file content directly. Useful for:

      - Referencing brand images and logos
      - - Loading HTML templates
        - - Pulling data files (JSON, CSV) for analysis
          - - Sharing generated artifacts across sessions
            - 
