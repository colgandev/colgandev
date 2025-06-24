document.addEventListener("DOMContentLoaded", function () {
  // Get the current tab and update its URL
  chrome.tabs.getCurrent(function (tab) {
    chrome.tabs.update(tab.id, {
      url: "http://localhost:4444/zettel/cards/create/",
    });
  });
});
