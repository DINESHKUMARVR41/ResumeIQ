const input = document.getElementById("resumeInput");
const dropZone = document.getElementById("dropZone");
const fileName = document.getElementById("fileName");
const analyzeButton = document.getElementById("analyzeButton");
const status = document.getElementById("status");

let selectedFile = null;

input.addEventListener("change", () => {
  selectedFile = input.files[0] || null;
  updateFile();
});

["dragenter", "dragover"].forEach(eventName => {
  dropZone.addEventListener(eventName, event => {
    event.preventDefault();
    dropZone.classList.add("dragging");
  });
});

["dragleave", "drop"].forEach(eventName => {
  dropZone.addEventListener(eventName, event => {
    event.preventDefault();
    dropZone.classList.remove("dragging");
  });
});

dropZone.addEventListener("drop", event => {
  const file = event.dataTransfer.files[0];
  if (file && file.type === "application/pdf") {
    selectedFile = file;
    updateFile();
  } else {
    status.textContent = "Please select a PDF file.";
  }
});

function updateFile() {
  if (!selectedFile) {
    fileName.textContent = "No file selected";
    analyzeButton.disabled = true;
    return;
  }

  fileName.textContent = `${selectedFile.name} · ${(selectedFile.size / 1024).toFixed(1)} KB`;
  analyzeButton.disabled = false;
  status.textContent = "Resume selected. Ready for analysis.";
}

analyzeButton.addEventListener("click", async () => {
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append("file", selectedFile);

  analyzeButton.disabled = true;
  status.textContent = "Sending resume to ResumeIQ...";

  try {
    const response = await fetch("http://127.0.0.1:8000/api/resume/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("Backend returned an error.");

    const data = await response.json();
    renderResults(data);
    status.textContent = "Analysis completed.";
  } catch (error) {
    status.textContent = "Backend is not running yet. Start FastAPI, then try again.";
  } finally {
    analyzeButton.disabled = false;
  }
});

function renderResults(data) {
  document.getElementById("score").textContent = `${data.analysis.score}/100`;
  document.getElementById("skillsCount").textContent = data.resume.skills.length;
  document.getElementById("wordCount").textContent = data.analysis.word_count;
  document.getElementById("sectionCount").textContent = data.analysis.detected_sections.length;

  document.getElementById("candidateName").textContent = data.resume.name || "Not detected";
  document.getElementById("candidateEmail").textContent = data.resume.email || "Not detected";
  document.getElementById("candidatePhone").textContent = data.resume.phone || "Not detected";

  const skillsList = document.getElementById("skillsList");
  skillsList.innerHTML = "";

  if (!data.resume.skills.length) {
    skillsList.innerHTML = '<span class="empty">No skills detected</span>';
    return;
  }

  data.resume.skills.forEach(skill => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = skill;
    skillsList.appendChild(chip);
  });
}
