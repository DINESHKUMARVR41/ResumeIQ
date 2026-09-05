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

// Small helper: never print null/undefined/empty values to the UI.
function displayValue(value) {
  if (value === null || value === undefined || value === "") {
    return "Not detected";
  }
  return value;
}

function renderResults(data) {
  const resume = data.resume;
  const candidate = resume.candidate || {};
  const score = resume.score || { total: 0, breakdown: {} };
  const breakdown = score.breakdown || {};

  // --- Metric cards ---
  document.getElementById("score").textContent = `${score.total}/100`;
  document.getElementById("skillsCount").textContent = resume.skills.length;
  document.getElementById("wordCount").textContent = resume.word_count;
  document.getElementById("sectionCount").textContent = resume.sections.length;

  // --- Candidate info ---
  document.getElementById("candidateName").textContent = displayValue(candidate.name);
  document.getElementById("candidateEmail").textContent = displayValue(candidate.email);
  document.getElementById("candidatePhone").textContent = displayValue(candidate.phone);

  // --- Skills chips ---
  const skillsList = document.getElementById("skillsList");
  skillsList.innerHTML = "";

  if (!resume.skills.length) {
    skillsList.innerHTML = '<span class="empty">No skills detected</span>';
  } else {
    resume.skills.forEach(skill => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = skill;
      skillsList.appendChild(chip);
    });
  }

  // --- Score breakdown ---
  document.getElementById("scoreContact").textContent = displayValue(breakdown.contact_information);
  document.getElementById("scoreSections").textContent = displayValue(breakdown.sections);
  document.getElementById("scoreSkills").textContent = displayValue(breakdown.skills);
  document.getElementById("scoreProjects").textContent = displayValue(breakdown.projects_or_experience);
  document.getElementById("scoreCerts").textContent = displayValue(breakdown.certifications_or_achievements);
}
