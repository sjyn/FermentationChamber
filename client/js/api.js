function fetchCurrentState() {
  const url = 'http://localhost:8081/control'
  _getRequest(url, (jsonObj) => {
    // @TODO -- make this nicer
    document.getElementById('current-state-container').innerText = JSON.stringify(jsonObj);
  });
}

function _getRequest(urlString, callbackFcn) {
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200)
      callbackFcn(JSON.parse(xmlHttp.responseText));
  }
  xmlHttp.open("GET", urlString, true); // true for asynchronous
  xmlHttp.send(null);
}

function _postRequest(urlString, bodyObj, callbackFcn) {
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.setRequestHeader('Content-Type', 'application/json')
  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200)
      callbackFcn(JSON.parse(xmlHttp.responseText));
  }
  xmlHttp.open("POST", urlString, true); // true for asynchronous
  xmlHttp.send(JSON.stringify(bodyObj));
}
