// =====================================================
// ResumeIQ Frontend
// =====================================================

const API_URL = "http://127.0.0.1:8000";

const input = document.getElementById("resumeInput");
const dropZone = document.getElementById("dropZone");
const fileName = document.getElementById("fileName");
const analyzeButton = document.getElementById("analyzeButton");
const status = document.getElementById("status");

let selectedFile = null;


// =====================================================
// RESUME FILE UPLOAD
// =====================================================

if (input) {
  input.addEventListener("change", () => {
    selectedFile = input.files[0] || null;
    updateFile();
  });
}


// Drag and drop
if (dropZone) {

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

      if (status) {
        status.textContent = "Please select a PDF file.";
      }

    }

  });

}


// =====================================================
// UPDATE SELECTED FILE
// =====================================================

function updateFile() {

  if (!selectedFile) {

    if (fileName) {
      fileName.textContent = "No file selected";
    }

    if (analyzeButton) {
      analyzeButton.disabled = true;
    }

    return;
  }


  if (fileName) {

    fileName.textContent =
      `${selectedFile.name} · ${(selectedFile.size / 1024).toFixed(1)} KB`;

  }


  if (analyzeButton) {
    analyzeButton.disabled = false;
  }


  if (status) {

    status.textContent =
      "Resume selected. Ready for analysis.";

  }

}


// =====================================================
// BASIC RESUME ANALYSIS
// =====================================================

if (analyzeButton) {

  analyzeButton.addEventListener("click", async () => {

    if (!selectedFile) {
      return;
    }


    const formData = new FormData();

    formData.append(
      "file",
      selectedFile
    );


    analyzeButton.disabled = true;


    if (status) {

      status.textContent =
        "Sending resume to ResumeIQ...";

    }


    try {

      const response = await fetch(
        `${API_URL}/api/resume/analyze`,
        {
          method: "POST",
          body: formData
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Backend returned an error."
        );

      }


      renderResults(data);


      if (status) {

        status.textContent =
          "Analysis completed.";

      }

    }

    catch (error) {

      console.error(
        "Resume analysis error:",
        error
      );


      if (status) {

        status.textContent =
          error.message ||
          "Backend is not running yet. Start FastAPI, then try again.";

      }

    }

    finally {

      analyzeButton.disabled = false;

    }

  });

}


// =====================================================
// HELPER
// =====================================================

function displayValue(value) {

  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {

    return "Not detected";

  }

  return value;

}


// Safely convert something into an array
function safeArray(value) {

  return Array.isArray(value)
    ? value
    : [];

}


// Safely convert something into an object
function safeObject(value) {

  if (
    value &&
    typeof value === "object" &&
    !Array.isArray(value)
  ) {

    return value;

  }

  return {};

}


// =====================================================
// RENDER BASIC RESUME RESULTS
// =====================================================

function renderResults(data) {

  const resume =
    data.resume || {};


  const candidate =
    resume.candidate || {};


  const score =
    resume.score || {
      total: 0,
      breakdown: {}
    };


  const breakdown =
    score.breakdown || {};


  const resumeSkills =
    safeArray(resume.skills);


  const resumeSections =
    safeArray(resume.sections);


  // ---------------------------------------------------
  // Metric cards
  // ---------------------------------------------------

  const scoreElement =
    document.getElementById("score");

  if (scoreElement) {

    scoreElement.textContent =
      `${score.total || 0}/100`;

  }


  const skillsCount =
    document.getElementById("skillsCount");

  if (skillsCount) {

    skillsCount.textContent =
      resumeSkills.length;

  }


  const wordCount =
    document.getElementById("wordCount");

  if (wordCount) {

    wordCount.textContent =
      resume.word_count || 0;

  }


  const sectionCount =
    document.getElementById("sectionCount");

  if (sectionCount) {

    sectionCount.textContent =
      resumeSections.length;

  }


  // ---------------------------------------------------
  // Candidate information
  // ---------------------------------------------------

  const candidateName =
    document.getElementById("candidateName");

  if (candidateName) {

    candidateName.textContent =
      displayValue(candidate.name);

  }


  const candidateEmail =
    document.getElementById("candidateEmail");

  if (candidateEmail) {

    candidateEmail.textContent =
      displayValue(candidate.email);

  }


  const candidatePhone =
    document.getElementById("candidatePhone");

  if (candidatePhone) {

    candidatePhone.textContent =
      displayValue(candidate.phone);

  }


  // ---------------------------------------------------
  // Skills
  // ---------------------------------------------------

  const skillsList =
    document.getElementById("skillsList");


  if (skillsList) {

    skillsList.innerHTML = "";


    if (resumeSkills.length === 0) {

      skillsList.innerHTML =
        '<span class="empty">No skills detected</span>';

    }

    else {

      resumeSkills.forEach(skill => {

        const chip =
          document.createElement("span");


        chip.className =
          "chip";


        chip.textContent =
          skill;


        skillsList.appendChild(
          chip
        );

      });

    }

  }


  // ---------------------------------------------------
  // Score breakdown
  // ---------------------------------------------------

  const scoreContact =
    document.getElementById("scoreContact");

  if (scoreContact) {

    scoreContact.textContent =
      displayValue(
        breakdown.contact_information
      );

  }


  const scoreSections =
    document.getElementById("scoreSections");

  if (scoreSections) {

    scoreSections.textContent =
      displayValue(
        breakdown.sections
      );

  }


  const scoreSkills =
    document.getElementById("scoreSkills");

  if (scoreSkills) {

    scoreSkills.textContent =
      displayValue(
        breakdown.skills
      );

  }


  const scoreProjects =
    document.getElementById("scoreProjects");

  if (scoreProjects) {

    scoreProjects.textContent =
      displayValue(
        breakdown.projects_or_experience
      );

  }


  const scoreCerts =
    document.getElementById("scoreCerts");

  if (scoreCerts) {

    scoreCerts.textContent =
      displayValue(
        breakdown.certifications_or_achievements
      );

  }

}


// =====================================================
// ATS MATCHING MODULE
// =====================================================

const atsAnalyzeBtn =
  document.getElementById("atsAnalyzeBtn");


const jobDescription =
  document.getElementById("jobDescription");


const atsResults =
  document.getElementById("atsResults");


const atsStatus =
  document.getElementById("atsStatus");


// -----------------------------------------------------
// ATS BUTTON
// -----------------------------------------------------

if (atsAnalyzeBtn) {

  atsAnalyzeBtn.addEventListener(
    "click",
    analyzeATS
  );

}


// =====================================================
// ANALYZE ATS
// =====================================================

async function analyzeATS() {

  // ---------------------------------------------------
  // Check resume
  // ---------------------------------------------------

  if (!selectedFile) {

    showATSStatus(
      "Please upload a resume first.",
      true
    );

    return;

  }


  // ---------------------------------------------------
  // Check job description
  // ---------------------------------------------------

  const jobText =
    jobDescription
      ? jobDescription.value.trim()
      : "";


  if (!jobText) {

    showATSStatus(
      "Please enter a job description.",
      true
    );

    return;

  }


  // ---------------------------------------------------
  // Button state
  // ---------------------------------------------------

  atsAnalyzeBtn.disabled = true;

  atsAnalyzeBtn.textContent =
    "Analyzing ATS Match...";


  showATSStatus(
    "Comparing your resume with the job description...",
    false
  );


  // ---------------------------------------------------
  // Form data
  // ---------------------------------------------------

  const formData =
    new FormData();


  formData.append(
    "file",
    selectedFile
  );


  formData.append(
    "job_description",
    jobText
  );


  try {

    // -------------------------------------------------
    // API request
    // -------------------------------------------------

    const response =
      await fetch(
        `${API_URL}/api/ats/analyze`,
        {
          method: "POST",
          body: formData
        }
      );


    // -------------------------------------------------
    // Read response
    // -------------------------------------------------

    const data =
      await response.json();


    console.log(
      "ATS API response:",
      data
    );


    // -------------------------------------------------
    // Error handling
    // -------------------------------------------------

    if (!response.ok) {

      throw new Error(
        data.detail ||
        "ATS analysis failed."
      );

    }


    // -------------------------------------------------
    // Get ATS result
    // -------------------------------------------------

    /*
       Your backend may return:

       {
         "ats": {...}
       }

       or directly:

       {
         "score": ...,
         ...
       }

       So we support both.
    */

    const ats =
      data.ats || data;


    // -------------------------------------------------
    // Render result
    // -------------------------------------------------

    renderATSResults(
      ats
    );


    if (atsResults) {

      atsResults.hidden = false;


      atsResults.scrollIntoView({
        behavior: "smooth"
      });

    }


    showATSStatus(
      "ATS analysis completed successfully.",
      false
    );

  }


  catch (error) {

    console.error(
      "ATS analysis error:",
      error
    );


    showATSStatus(
      error.message ||
      "ATS analysis failed.",
      true
    );

  }


  finally {

    atsAnalyzeBtn.disabled = false;

    atsAnalyzeBtn.textContent =
      "Analyze ATS Match";

  }

}


// =====================================================
// RENDER ATS RESULTS
// =====================================================

function renderATSResults(ats) {

  console.log("ATS result received:", ats);

  // =====================================================
  // SAFELY READ ATS SCORE
  // =====================================================

  const score = Number(
    ats?.score ??
    ats?.ats_score ??
    ats?.total_score ??
    0
  );

  // =====================================================
  // SCORE
  // =====================================================

  const scoreElement =
    document.getElementById("atsScore");

  if (scoreElement) {
    scoreElement.textContent =
      `${Math.round(score)}/100`;
  }

  // =====================================================
  // SCORE MESSAGE
  // =====================================================

  const message =
    document.getElementById("atsScoreMessage");

  if (message) {
    message.textContent =
      getATSMessage(score);
  }

  // =====================================================
  // SKILLS
  // =====================================================

  const skills =
    ats?.skills || {};

  const matchingSkills =
    safeArray(
      skills.matched ??
      skills.matching ??
      skills.matching_skills ??
      ats?.matching_skills
    );

  const missingSkills =
    safeArray(
      skills.missing ??
      skills.missing_skills ??
      ats?.missing_skills
    );

  const resumeOnlySkills =
    safeArray(
      skills.resume_only ??
      skills.resume_only_skills ??
      ats?.resume_only_skills
    );

  // =====================================================
  // KEYWORDS
  // =====================================================

  const keywords =
    ats?.keywords || {};

  const matchedKeywords =
    safeArray(
      keywords.matched ??
      keywords.matching ??
      keywords.matched_keywords ??
      ats?.matched_keywords
    );

  const missingKeywords =
    safeArray(
      keywords.missing ??
      keywords.missing_keywords ??
      ats?.missing_keywords
    );

  // =====================================================
  // COUNTS
  // =====================================================

  const matchingSkillsCount =
    document.getElementById(
      "matchingSkillsCount"
    );

  if (matchingSkillsCount) {
    matchingSkillsCount.textContent =
      matchingSkills.length;
  }

  const missingSkillsCount =
    document.getElementById(
      "missingSkillsCount"
    );

  if (missingSkillsCount) {
    missingSkillsCount.textContent =
      missingSkills.length;
  }

  const matchedKeywordsCount =
    document.getElementById(
      "matchedKeywordsCount"
    );

  if (matchedKeywordsCount) {
    matchedKeywordsCount.textContent =
      matchedKeywords.length;
  }

  // =====================================================
  // RENDER SKILL CHIPS
  // =====================================================

  renderSkillChips(
    "matchingSkills",
    matchingSkills
  );

  renderSkillChips(
    "missingSkills",
    missingSkills
  );

  renderSkillChips(
    "resumeOnlySkills",
    resumeOnlySkills
  );

  // =====================================================
  // RENDER KEYWORDS
  // =====================================================

  renderSkillChips(
    "matchedKeywords",
    matchedKeywords
  );

  renderSkillChips(
    "missingKeywords",
    missingKeywords
  );

  // =====================================================
  // SCORE BREAKDOWN
  // =====================================================

  const breakdown =
    ats?.score_breakdown ??
    ats?.breakdown ??
    {};

  renderATSBreakdown(
    breakdown
  );
}


// =====================================================
// RENDER SKILL CHIPS
// =====================================================

function renderSkillChips(
  elementId,
  items
) {

  const container =
    document.getElementById(
      elementId
    );


  if (!container) {
    return;
  }


  // Always convert to array
  items =
    safeArray(items);


  container.innerHTML = "";


  // ---------------------------------------------------
  // No results
  // ---------------------------------------------------

  if (items.length === 0) {

    const empty =
      document.createElement(
        "span"
      );


    empty.className =
      "skill-chip";


    empty.textContent =
      "None detected";


    container.appendChild(
      empty
    );


    return;

  }


  // ---------------------------------------------------
  // Create chips
  // ---------------------------------------------------

  items.forEach(item => {

    const chip =
      document.createElement(
        "span"
      );


    chip.className =
      "skill-chip";


    chip.textContent =
      item;


    container.appendChild(
      chip
    );

  });

}


// =====================================================
// ATS SCORE BREAKDOWN
// =====================================================

function renderATSBreakdown(breakdown) {

  const container =
    document.getElementById(
      "atsScoreBreakdown"
    );

  if (!container) {
    return;
  }

  container.innerHTML = "";

  // Make sure breakdown is an object
  if (
    !breakdown ||
    typeof breakdown !== "object" ||
    Array.isArray(breakdown)
  ) {

    const row =
      document.createElement("div");

    row.className =
      "score-row";

    row.innerHTML = `
      <span>Breakdown</span>
      <strong>Not available</strong>
    `;

    container.appendChild(row);

    return;
  }

  const entries =
    Object.entries(breakdown);

  if (entries.length === 0) {

    const row =
      document.createElement("div");

    row.className =
      "score-row";

    row.innerHTML = `
      <span>Breakdown</span>
      <strong>Not available</strong>
    `;

    container.appendChild(row);

    return;
  }

  entries.forEach(([key, value]) => {

    const row =
      document.createElement("div");

    row.className =
      "score-row";

    let displayValue = value;

    // If backend returns an object such as:
    // { raw: 90, weight: 60, contribution: 54 }
    if (
      value &&
      typeof value === "object"
    ) {

      if (value.contribution !== undefined) {

        displayValue =
          `${value.contribution}`;

      }

      else if (value.score !== undefined) {

        displayValue =
          `${value.score}`;

      }

      else if (value.raw !== undefined) {

        displayValue =
          `${value.raw}`;

      }

      else {

        displayValue =
          JSON.stringify(value);

      }

    }

    row.innerHTML = `
      <span>
        ${formatATSLabel(key)}
      </span>

      <strong>
        ${displayValue}
      </strong>
    `;

    container.appendChild(row);

  });

}


// =====================================================
// FORMAT ATS LABEL
// =====================================================

function formatATSLabel(
  value
) {

  return String(value)
    .replaceAll(
      "_",
      " "
    )
    .replace(
      /\b\w/g,
      char =>
        char.toUpperCase()
    );

}


// =====================================================
// ATS SCORE MESSAGE
// =====================================================

function getATSMessage(
  score
) {

  if (score >= 80) {

    return (
      "Excellent match. Your resume aligns strongly with this job."
    );

  }


  if (score >= 60) {

    return (
      "Good match. A few improvements could make your resume stronger."
    );

  }


  if (score >= 40) {

    return (
      "Moderate match. Consider addressing the missing skills and keywords."
    );

  }


  return (
    "Low match. Your resume needs significant alignment with this job description."
  );

}


// =====================================================
// ATS STATUS
// =====================================================

function showATSStatus(
  message,
  isError
) {

  if (!atsStatus) {
    return;
  }


  atsStatus.textContent =
    message;


  atsStatus.classList.toggle(
    "error",
    isError
  );

}