async function loadData() {
  const res = await fetch("data.json");
  return res.json();
}

function getId() {
  return new URLSearchParams(location.search).get("id");
}

async function sha256(text) {
  const enc = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", enc);
  return [...new Uint8Array(hash)]
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");
}

let ITEM = null;

async function init() {
  const db = await loadData();
  const id = getId();

  if (!db.items[id]) {
    document.body.innerHTML = "<h3>Item not found</h3>";
    return;
  }

  ITEM = db.items[id];

  document.getElementById("owner").innerText = "Owner: " + db.meta.owner;
  document.getElementById("name").innerText = ITEM.name;
  document.getElementById("code").innerText = "Code: " + id;
  document.getElementById("route").innerText = "Route: " + db.meta.route;
  document.getElementById("flight").innerText = "Flight: " + db.meta.flight;
}

async function verify() {
  const input = document.getElementById("pass").value;
  const hash = await sha256(input);

  const result = document.getElementById("result");

  if (hash === ITEM.challenge.hash) {
    result.innerText = "✔ VERIFIED";
    result.style.color = "lightgreen";
  } else {
    result.innerText = "✖ NOT VERIFIED";
    result.style.color = "red";
  }
}

init();