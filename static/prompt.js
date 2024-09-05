const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const importButton = document.getElementById("import-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);

const handleImportClick = () => {
  // Create an input element dynamically
  const inputElement = document.createElement("input");
  inputElement.type = "file";
  inputElement.accept = ".pdf, .txt, .html, .md, .docx"; // Accepter PDF, TXT, HTML MD et DOCX

  // Trigger the file selection dialog
  inputElement.click();

  // Listen for file selection
  inputElement.addEventListener("change", async () => {
    const file = inputElement.files[0];
    if (file) {
      // Create a FormData object and append the selected file
      const formData = new FormData();
      formData.append("file", file);

      try {
        // Send the file to the API
        const response = await fetch("/file", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          appendAIMessage(() => Promise.resolve(`Fichier ajouté avec succès : ${result.response}`));
        } else {
          appendAIMessage(() => Promise.resolve("Impossible de télécharger le fichier !"));
        }
      } catch (error) {
        appendAIMessage(() => Promise.resolve("Le téléchargement du fichier a échoué"));
      }
    }
  });
}

importButton.addEventListener("click", handleImportClick);