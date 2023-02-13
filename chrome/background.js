chrome.runtime.onConnect.addListener(function (port) {
    port.onMessage.addListener(function (message) {
      if (message.action === "closeTab") {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          chrome.tabs.remove(tabs[0].id);
        });
      }
    });
  });