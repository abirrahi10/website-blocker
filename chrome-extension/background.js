chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
      const tab = await chrome.tabs.get(activeInfo.tabId);
      console.log("Tab:", tab);
      const newUrl = tab.url;
      console.log("New URL:", newUrl);

      const response = await fetch("http://127.0.0.1:5000/send_url", {
          method: "POST",
          body: new URLSearchParams({
              url: newUrl,
              timestamp: Math.floor(Date.now() / 1000),
          }),
      });

      const responseData = await response.text();
      console.log("Response:", responseData);
  } catch (error) {
      console.error("Error:", error);
  }
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (tab.active && changeInfo.url) {
      console.log("Changed:", changeInfo.url);
      try {
          const response = await fetch("http://127.0.0.1:5000/send_url", {
              method: "POST",
              body: new URLSearchParams({
                  url: changeInfo.url,
                  timestamp: Math.floor(Date.now() / 1000),
              }),
          });

          const responseData = await response.text();
          console.log(responseData);
      } catch (error) {
          console.error("Error:", error);
      }
  }
});

const tabToUrl = {};

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url) {
      tabToUrl[tabId] = tab.url;
      console.log(tabToUrl);
  }
});

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  if (tabToUrl[tabId]) {
      const removedUrl = tabToUrl[tabId];
      console.log(removedUrl);

      fetch("http://127.0.0.1:5000/quit_url", {
          method: "POST",
          body: new URLSearchParams({
              url: removedUrl,
              timestamp: Math.floor(Date.now() / 1000),
          }),
      })
          .then(response => response.text())
          .then(responseText => {
              console.log(responseText);
          })
          .catch(error => {
              console.error("Error:", error);
          });

      delete tabToUrl[tabId];
  }
});