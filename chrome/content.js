document.addEventListener("keydown", async function (event) {
    if (event.ctrlKey && event.shiftKey && event.code === "KeyB") {
        chrome.storage.sync.get(["port", "key"], async function (items) {
            try {
                await fetch(`http://localhost:${items.port}/block?url=${location.hostname}&key=${items.key}`,
        {mode: 'no-cors'});
                const backgroundPage = chrome.runtime.connect({ name: "closeTab" });
                backgroundPage.postMessage({ action: "closeTab" });
            } catch (error) {
                console.error(error);
            }
          });
    }
  });