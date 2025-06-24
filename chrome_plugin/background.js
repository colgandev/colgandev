// Listen for keyboard shortcuts
chrome.commands.onCommand.addListener(async (command) => {
  const [activeTab] = await chrome.tabs.query({
    active: true,
    currentWindow: true,
  });
  if (!activeTab || !activeTab.url) return;

  const shouldCloseTab = command === "save-page-and-close";
  await savePageAsZettel(activeTab, shouldCloseTab);
});

async function savePageAsZettel(tab, shouldCloseTab = false) {
  if (!tab.url) return;

  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractPageData,
    });

    const pageData = results[0].result;

    const csrfResponse = await fetch("http://localhost:4444/_/csrf-token/");
    const csrfToken = await csrfResponse.text();

    const formData = new FormData();
    formData.append("title", pageData.title);
    formData.append("content", pageData.description);
    formData.append("target_type", "zettel.Bookmark");
    formData.append("url", tab.url);
    formData.append("csrfmiddlewaretoken", csrfToken);

    const screenshotDataUrl = await chrome.tabs.captureVisibleTab(
      tab.windowId,
      { format: "png" }
    );
    const screenshotBlob = dataURLtoBlob(screenshotDataUrl);
    formData.append("image", screenshotBlob, "screenshot.png");

    await fetch("http://localhost:4444/_/content/create/", {
      method: "POST",
      body: formData,
    });

    // Close the tab if requested
    if (shouldCloseTab) {
      await chrome.tabs.remove(tab.id);
    }

    console.log("Successfully saved page as zettel");
  } catch (error) {
    console.error("Error creating zettel bookmark:", error);
  }
}

function extractPageData() {
  const title = document.querySelector("title")?.textContent || "";
  const description =
    document.querySelector('meta[name="description"]')?.content || "";
  return { title, description };
}

function dataURLtoBlob(dataURL) {
  const arr = dataURL.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

// Keep the original bookmark listener if you still want that functionality
chrome.bookmarks.onCreated.addListener(async (id, bookmark) => {
  if (!bookmark.url) return;

  const [tab] = await chrome.tabs.query({ url: bookmark.url });
  if (!tab) return;

  await savePageAsZettel(tab, true); // Close tab when bookmarking
});
