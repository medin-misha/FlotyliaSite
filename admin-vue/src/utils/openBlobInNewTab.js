const escapeHtml = (value) =>
  String(value).replace(/[&<>"']/g, (char) => {
    const entities = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    }

    return entities[char] || char
  })

const writeWindowMarkup = (targetWindow, markup, title = 'File') => {
  targetWindow.document.open()
  targetWindow.document.write(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(title)}</title>
    <style>
      :root {
        color-scheme: light;
        font-family: Arial, sans-serif;
      }

      body {
        margin: 0;
        min-height: 100vh;
        background: #f5f5f5;
        color: #111827;
      }

      .viewer-shell {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
      }

      .viewer-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 12px 16px;
        background: #ffffff;
        border-bottom: 1px solid #d1d5db;
      }

      .viewer-toolbar strong {
        font-size: 14px;
        font-weight: 600;
      }

      .viewer-toolbar a {
        color: #b91c1c;
        text-decoration: none;
        font-size: 14px;
        font-weight: 600;
      }

      .viewer-content {
        flex: 1;
        min-height: 0;
      }

      .viewer-frame,
      .viewer-image {
        width: 100%;
        height: calc(100vh - 57px);
        border: 0;
      }

      .viewer-image {
        object-fit: contain;
        background: #111827;
      }

      .viewer-message {
        display: grid;
        place-items: center;
        min-height: 100vh;
        padding: 24px;
        text-align: center;
      }

      .viewer-message p {
        margin: 0;
        font-size: 14px;
      }
    </style>
  </head>
  <body>${markup}</body>
</html>`)
  targetWindow.document.close()
}

const buildViewerMarkup = (blobUrl, mimeType) => {
  const safeBlobUrl = escapeHtml(blobUrl)

  if (mimeType.startsWith('image/')) {
    return `
      <main class="viewer-shell">
        <header class="viewer-toolbar">
          <strong>Preview</strong>
          <a href="${safeBlobUrl}" download>Download</a>
        </header>
        <section class="viewer-content">
          <img class="viewer-image" src="${safeBlobUrl}" alt="Preview" />
        </section>
      </main>
    `
  }

  return `
    <main class="viewer-shell">
      <header class="viewer-toolbar">
        <strong>Preview</strong>
        <a href="${safeBlobUrl}" download>Download</a>
      </header>
      <section class="viewer-content">
        <iframe class="viewer-frame" src="${safeBlobUrl}" title="File preview"></iframe>
      </section>
    </main>
  `
}

export const openBlobInNewTab = async (loadBlob, title = 'File') => {
  const openedWindow = window.open('', '_blank')

  if (!openedWindow) {
    throw new Error('Popup window was blocked by the browser')
  }

  writeWindowMarkup(
    openedWindow,
    '<main class="viewer-message"><p>Loading file...</p></main>',
    title,
  )

  try {
    const blob = await loadBlob()
    const blobUrl = URL.createObjectURL(blob)
    const mimeType = blob.type || 'application/octet-stream'

    writeWindowMarkup(openedWindow, buildViewerMarkup(blobUrl, mimeType), title)
    openedWindow.opener = null
    openedWindow.addEventListener('beforeunload', () => URL.revokeObjectURL(blobUrl), {
      once: true,
    })
    setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
  } catch (error) {
    writeWindowMarkup(
      openedWindow,
      '<main class="viewer-message"><p>Failed to load file.</p></main>',
      title,
    )
    throw error
  }
}
