/*
Cette fonction va prendre les données soumises dans le formulaire avec l'id "keyword-form" et envoie une requête POST à l'URL "/keywording" avec les données du formulaire (Mot clé) puis 
renvoie les résultats de la requete à la fonction displayResults. 
(Envoie au search engine les mots clés pour la recherche)
*/
document.getElementById("keyword-form").addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch("/keywording", {
      method: "POST",
      body: formData,
    }).then((response) => response.json())
      .then((data) => {
        displayResults(data);
    }).catch((error) => {
        console.error("Erreur:", error);
    });
});

/*
Cette fonction prend en paramètre les données reçus de la fontion précedente et les affiche dans le container avec l'id "results" sous forme de div.
(Affiche les résultats de la recherche)
*/
function displayResults(data) {
  var container = document.getElementById("results");
  container.innerHTML = "";
  data.forEach((item) => {
    var resultDiv = document.createElement("div");
    resultDiv.classList.add("result");
    resultDiv.innerHTML = `
                    <a href="${item.url}" target="_blank">
                    <div class="title">${item.title}</div>
                    <div class="description">${item.description}</div>
                    <div class="url">${item.url}</div>
                    </a>
                `;
    container.appendChild(resultDiv);
  });
}

/*
Cette fonction va prendre les données soumises dans le formulaire avec l'id "crawler-form" et envoie une requête POST à l'URL "/crawler" avec les données du formulaire (Lien de départ)
puis attend que le crawler fasse son travail (25s) renvoie les résultats de la requete à la fonction displayCrawlerResults. 
(Envoie au crawler le lien de départ pour le crawling)
*/
document.getElementById("crawler-form").addEventListener("submit", function (event) {
    event.preventDefault();
    testerCrawler();
});

function testerCrawler() {
  var countdownElement = document.getElementById("countdown");
  countdownElement.style.display = "block";
  var timeLeft = 25;

  var countdownTimer = setInterval(function () {
    timeLeft--;
    countdownElement.textContent = timeLeft;
    if (timeLeft <= 0) {
      clearInterval(countdownTimer);
      countdownElement.style.display = "none";
    }
  }, 1000);

  var formData = new FormData(document.getElementById("crawler-form"));
  fetch("/crawler", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Résultats", data);
      var resultDisplayCheck = setInterval(function () {
        if (timeLeft <= 0) {
          clearInterval(resultDisplayCheck);
          displayCrawlerResults(data.data);
        }
      }, 1000);
    })
    .catch((error) => {
      console.error("Erreur:", error);
    });
}

/*
Cette fonction prend en paramètre les données reçus de la fontion précedente et les affiche dans le container avec l'id "results-crawlers" sous forme de tableau. 
(Affiche les résultats du crawling (Mots clés, URL, Fréquence))
*/
function displayCrawlerResults(data) {
  var container = document.getElementById("results-crawlers");
  container.innerHTML = "";

  var scrollableContainer = document.createElement("div");
  scrollableContainer.style.height = "200px";
  scrollableContainer.style.overflowY = "auto"; 
  scrollableContainer.style.border = "1px solid black";

  var table = document.createElement("table");
  table.style.width = "100%";
  table.style.tableLayout = "fixed"; 

  var thead = document.createElement("thead");
  var headerRow = document.createElement("tr");
  ["Mot-clé", "URL", "Fréquence"].forEach((headerText) => {
    var headerCell = document.createElement("th");
    headerCell.textContent = headerText;
    headerCell.style.maxWidth = "200px";
    headerCell.style.wordWrap = "break-word";
    headerRow.appendChild(headerCell);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  var tbody = document.createElement("tbody");
  tbody.style.display = "table-row-group";

  data.forEach((item) => {
    var isFirstUrl = true;
    Object.entries(item[1]).forEach(([url, frequency]) => {
      var row = document.createElement("tr");
      if (isFirstUrl) {
        var keywordCell = document.createElement("td");
        keywordCell.textContent = item[0];
        keywordCell.style.maxWidth = "200px";
        keywordCell.style.wordWrap = "break-word";
        row.appendChild(keywordCell);
        isFirstUrl = false;
      } else {
        var emptyCell = document.createElement("td");
        emptyCell.style.maxWidth = "200px";
        emptyCell.style.wordWrap = "break-word";
        row.appendChild(emptyCell);
      }

      var urlCell = document.createElement("td");
      urlCell.textContent = url;
      urlCell.style.maxWidth = "200px";
      urlCell.style.wordWrap = "break-word";
      row.appendChild(urlCell);

      var freqCell = document.createElement("td");
      freqCell.textContent = frequency.toFixed(6);
      freqCell.style.maxWidth = "200px";
      freqCell.style.wordWrap = "break-word";
      row.appendChild(freqCell);

      tbody.appendChild(row);
    });
  });
  table.appendChild(tbody);

  scrollableContainer.appendChild(table);
  container.appendChild(scrollableContainer);
}

/*
Cette fonction va prendre les données soumises dans le formulaire avec l'id "indexation-crawler-form" et envoie une requête POST à l'URL "/keywordingClient" avec les données du formulaire (Mot clé) puis 
renvoie les résultats de la requete à la fonction displayCrawlerKeywordsResults. 
(Envoie au search engine les mots clés pour la recherche mais avec les données de votre propre crawler)
*/
document.getElementById("indexation-crawler-form").addEventListener("submit", function (event) {
    event.preventDefault();
    testerCrawlerKeywords();
});

function testerCrawlerKeywords() {
  var formData = new FormData(
    document.getElementById("indexation-crawler-form")
  );
  fetch("/keywordingClient", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Result", data);
      displayCrawlerKeywordsResults(data);
    })
    .catch((error) => {
      console.error("Erreur:", error);
    });
}

/*
Cette fonction prend en paramètre les données reçus de la fontion précedente et les affiche dans le container avec l'id "index-crawler-results" sous forme de div.
(Affiche les résultats de la recherche avec les données de votre propre crawler)
*/
function displayCrawlerKeywordsResults(data) {
  console.log(data);
  var container = document.getElementById("index-crawler-results");
  container.innerHTML = "";
  data.forEach((item) => {
    var resultDiv = document.createElement("div");
    resultDiv.classList.add("result");
    resultDiv.innerHTML = `
            <a href="${item.url}" target="_blank">
            <div class="title">${item.title}</div>
            <div class="description">${item.description}</div>
            <div class="url">${item.url}</div>
            </a>
        `;
    container.appendChild(resultDiv);
  });
}
