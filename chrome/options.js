document.addEventListener("DOMContentLoaded", function () {
    chrome.storage.sync.get(["port", "key"], function (items) {
      document.querySelector("#port").value = items.port || 8080;
      document.querySelector("#key").value = items.key || "mysecretkey";
    });
  });
  
  document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault();
    var port = document.querySelector("#port").value;
    var key = document.querySelector("#key").value;
    chrome.storage.sync.set({ port: port, key: key }, function () {
      console.log("Options saved.");
    });
  });