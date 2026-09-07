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
let resumeAnalysis = null;
let atsAnalysis = null;
let skillGapAnalysis = null;
let careerAnalysis = null;
let assistantMessages = [];

const downloadReportButton = document.getElementById("downloadReportButton");
const reportDownloadStatus = document.getElementById("reportDownloadStatus");


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


      resumeAnalysis = data;
      atsAnalysis = null;
      skillGapAnalysis = null;
      careerAnalysis = null;
      assistantMessages = [];
      setReportButtonEnabled(true);
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

    atsAnalysis = ats;
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

// =====================================================
// MODULE 04 — SKILL GAP
// =====================================================

const skillGapAnalyzeBtn = document.getElementById("skillGapAnalyzeBtn");
const skillGapJobDescription = document.getElementById("skillGapJobDescription");
const skillGapResults = document.getElementById("skillGapResults");
const skillGapStatus = document.getElementById("skillGapStatus");

if (skillGapAnalyzeBtn) {
  skillGapAnalyzeBtn.addEventListener("click", analyzeSkillGap);
}

async function analyzeSkillGap() {
  if (!selectedFile) {
    showSkillGapStatus("Please upload a resume first.", true);
    return;
  }

  const jobText = skillGapJobDescription?.value.trim() || "";
  if (!jobText) {
    showSkillGapStatus("Please enter a target job description.", true);
    return;
  }

  skillGapAnalyzeBtn.disabled = true;
  skillGapAnalyzeBtn.textContent = "Analyzing Skill Gap...";
  showSkillGapStatus("Comparing your skills with the target role...", false);

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("job_description", jobText);

  try {
    const response = await fetch(`${API_URL}/api/skill-gap/analyze`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Skill gap analysis failed.");
    }

    skillGapAnalysis = data.skill_gap || data;
    renderSkillGapResults(skillGapAnalysis);

    if (skillGapResults) {
      skillGapResults.hidden = false;
      skillGapResults.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    showSkillGapStatus("Skill gap analysis completed.", false);
  } catch (error) {
    console.error("Skill gap error:", error);
    showSkillGapStatus(error.message || "Skill gap analysis failed.", true);
  } finally {
    skillGapAnalyzeBtn.disabled = false;
    skillGapAnalyzeBtn.textContent = "Analyze Skill Gap";
  }
}

function renderSkillGapResults(result) {
  const coverage = Number(result?.coverage || 0);
  const summary = safeObject(result?.summary);

  document.getElementById("skillGapCoverage").textContent = `${Math.round(coverage)}%`;
  document.getElementById("skillGapRequired").textContent = summary.required_skills ?? safeArray(result.required_skills).length;
  document.getElementById("skillGapMatched").textContent = summary.matched_skills ?? safeArray(result.matched_skills).length;
  document.getElementById("skillGapMissing").textContent = summary.missing_skills ?? safeArray(result.missing_skills).length;

  const message = result?.coverage_message || getSkillGapMessage(coverage);
  document.getElementById("skillGapCoverageMessage").textContent = message;

  renderSkillChips("skillGapMatchedSkills", result?.matched_skills || [], "matched");
  renderSkillChips("skillGapMissingSkills", result?.missing_skills || [], "missing");

  const details = document.getElementById("skillGapDetails");
  if (!details) return;
  details.innerHTML = "";

  const gaps = safeArray(result?.gaps);

  if (!gaps.length) {
    details.innerHTML = '<p class="empty">No significant skill gaps detected.</p>';
    return;
  }

  gaps.forEach(gap => {
    const item = document.createElement("div");
    item.className = "skill-gap-detail";

    const priority = String(gap.priority || "Medium").toLowerCase();
    const badgeClass = priority === "high" ? "priority-high" : priority === "low" ? "priority-low" : "priority-medium";

    item.innerHTML = `
      <div class="skill-gap-detail-head">
        <div>
          <span class="metric-label">${escapeHTML(gap.category || "Skill")}</span>
          <h4>${escapeHTML(gap.skill || "Unknown skill")}</h4>
        </div>
        <span class="${badgeClass}">${escapeHTML(gap.priority || "Medium")}</span>
      </div>
      <p>${escapeHTML(gap.reason || "This skill appears in the target requirements but was not detected in the resume.")}</p>
      <div class="learning-focus"><b>Learning focus:</b> ${escapeHTML(gap.learning_focus || "Build practical knowledge and demonstrate it in a project.")}</div>
    `;

    details.appendChild(item);
  });
}

function getSkillGapMessage(coverage) {
  if (coverage >= 80) return "Excellent coverage. Focus on depth and evidence.";
  if (coverage >= 60) return "Good coverage. A few targeted skills can strengthen your profile.";
  if (coverage >= 40) return "Moderate coverage. Prioritize the high-value missing skills.";
  return "Low coverage. Start with the highest-priority skills before applying.";
}

function showSkillGapStatus(message, isError) {
  if (!skillGapStatus) return;
  skillGapStatus.textContent = message;
  skillGapStatus.classList.toggle("error", Boolean(isError));
}


// =====================================================
// MODULE 05 — GEMINI CAREER INTELLIGENCE
// =====================================================

const careerAnalyzeBtn = document.getElementById("careerAnalyzeBtn");
const careerResults = document.getElementById("careerResults");
const careerStatus = document.getElementById("careerStatus");

if (careerAnalyzeBtn) {
  careerAnalyzeBtn.addEventListener("click", analyzeCareer);
}

async function analyzeCareer() {
  if (!selectedFile) {
    showCareerStatus("Please upload a resume first.", true);
    return;
  }

  careerAnalyzeBtn.disabled = true;
  careerAnalyzeBtn.textContent = "Gemini is analyzing...";
  showCareerStatus("Building your personalized career analysis...", false);

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(`${API_URL}/api/career/recommend`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Career analysis failed.");
    }

    careerAnalysis = { ai_analysis: data.ai_analysis || {}, career_engine: data.career_engine || {} };
    renderCareerResults(careerAnalysis.ai_analysis, careerAnalysis.career_engine);

    if (careerResults) {
      careerResults.hidden = false;
      careerResults.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    showCareerStatus("AI career analysis completed.", false);
  } catch (error) {
    console.error("Career AI error:", error);
    showCareerStatus(error.message || "Career analysis failed.", true);
  } finally {
    careerAnalyzeBtn.disabled = false;
    careerAnalyzeBtn.textContent = "Analyze Career with AI";
  }
}

function renderCareerResults(ai, engine) {
  const recommended = safeObject(ai.recommended_career);

  document.getElementById("recommendedCareer").textContent = recommended.title || "Not available";
  document.getElementById("careerReason").textContent = recommended.reason || "No recommendation reason returned.";
  document.getElementById("careerFitScore").textContent = `${Number(recommended.fit_score || 0)}%`;
  document.getElementById("careerSummary").textContent = ai.career_summary || "No summary returned.";

  renderSkillChips("careerStrengths", safeArray(ai.current_strengths), "matched");
  renderSkillChips("careerMissingSkills", safeArray(ai.missing_skills), "missing");

  const recommendedSkills = document.getElementById("careerRecommendedSkills");
  recommendedSkills.innerHTML = "";

  safeArray(ai.recommended_skills).forEach(item => {
    const row = document.createElement("div");
    row.className = "career-list-item";
    const priority = String(item.priority || "Medium").toLowerCase();
    const badge = priority === "high" ? "priority-high" : priority === "low" ? "priority-low" : "priority-medium";
    row.innerHTML = `
      <div><strong>${escapeHTML(item.skill || "")}</strong><p>${escapeHTML(item.reason || "")}</p></div>
      <span class="${badge}">${escapeHTML(item.priority || "Medium")}</span>
    `;
    recommendedSkills.appendChild(row);
  });

  const projects = document.getElementById("careerProjects");
  projects.innerHTML = "";

  safeArray(ai.recommended_projects).forEach((project, index) => {
    const card = document.createElement("div");
    card.className = "career-project";
    card.innerHTML = `
      <span class="project-number">0${index + 1}</span>
      <div>
        <h4>${escapeHTML(project.title || "Project")}</h4>
        <p>${escapeHTML(project.description || "")}</p>
        <div class="skills-list">${safeArray(project.skills).map(skill => `<span class="skill-chip">${escapeHTML(skill)}</span>`).join("")}</div>
      </div>
    `;
    projects.appendChild(card);
  });

  const roadmap = safeObject(ai.roadmap);
  renderRoadmap("roadmap30", roadmap.days_30);
  renderRoadmap("roadmap60", roadmap.days_60);
  renderRoadmap("roadmap90", roadmap.days_90);

  document.getElementById("careerAdvice").textContent = ai.final_advice || "No final advice returned.";
}

function renderRoadmap(elementId, items) {
  const container = document.getElementById(elementId);
  if (!container) return;

  container.innerHTML = "";
  const list = safeArray(items);

  if (!list.length) {
    container.innerHTML = '<p class="empty">No roadmap items returned.</p>';
    return;
  }

  const ul = document.createElement("ul");
  list.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
  container.appendChild(ul);
}

function showCareerStatus(message, isError) {
  if (!careerStatus) return;
  careerStatus.textContent = message;
  careerStatus.classList.toggle("error", Boolean(isError));
}


// =====================================================
// MODULE 06 — GROQ AI ASSISTANT
// =====================================================

const assistantQuestion = document.getElementById("assistantQuestion");
const assistantSendBtn = document.getElementById("assistantSendBtn");
const chatMessages = document.getElementById("chatMessages");
const assistantStatus = document.getElementById("assistantStatus");

if (assistantSendBtn) {
  assistantSendBtn.addEventListener("click", sendAssistantMessage);
}

if (assistantQuestion) {
  assistantQuestion.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendAssistantMessage();
    }
  });
}

async function sendAssistantMessage() {
  if (!selectedFile) {
    showAssistantStatus("Please upload a resume first.", true);
    return;
  }

  const question = assistantQuestion?.value.trim() || "";
  if (!question) {
    showAssistantStatus("Type a question first.", true);
    return;
  }

  addChatMessage("You", question, "user");
  assistantQuestion.value = "";
  assistantSendBtn.disabled = true;
  assistantSendBtn.textContent = "Thinking...";
  showAssistantStatus("ResumeIQ is preparing an answer...", false);

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("question", question);

  try {
    const response = await fetch(`${API_URL}/api/assistant/chat`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Assistant request failed.");
    }

    const answer = data.answer || "No answer returned.";
    addChatMessage("ResumeIQ", answer, "assistant");
    assistantMessages.push({ role: "user", content: question }, { role: "assistant", content: answer });
    showAssistantStatus("Answer generated.", false);
  } catch (error) {
    console.error("Assistant error:", error);
    addChatMessage("ResumeIQ", `Sorry, I couldn't answer that: ${error.message}`, "assistant");
    showAssistantStatus(error.message || "Assistant failed.", true);
  } finally {
    assistantSendBtn.disabled = false;
    assistantSendBtn.textContent = "Ask ResumeIQ";
  }
}

function addChatMessage(role, message, type) {
  if (!chatMessages) return;

  const wrapper = document.createElement("div");
  wrapper.className = `chat-message ${type}-message`;

  const roleElement = document.createElement("span");
  roleElement.className = "chat-role";
  roleElement.textContent = role;

  const textElement = document.createElement("p");
  textElement.textContent = message;

  wrapper.appendChild(roleElement);
  wrapper.appendChild(textElement);
  chatMessages.appendChild(wrapper);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showAssistantStatus(message, isError) {
  if (!assistantStatus) return;
  assistantStatus.textContent = message;
  assistantStatus.classList.toggle("error", Boolean(isError));
}


// =====================================================
// SHARED HTML ESCAPING
// =====================================================

function escapeHTML(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}


// =====================================================
// FULL REPORT DOWNLOAD
// =====================================================
function setReportButtonEnabled(enabled) {
  if (!downloadReportButton) return;
  downloadReportButton.disabled = !enabled;
  if (reportDownloadStatus) {
    reportDownloadStatus.textContent = enabled
      ? "Your report is ready to download."
      : "Complete resume analysis to enable the report.";
  }
}

if (downloadReportButton) {
  downloadReportButton.addEventListener("click", async () => {
    console.log("ResumeIQ: Download Full Report clicked");

    if (!resumeAnalysis) {
      reportDownloadStatus.textContent =
        "Please analyze your resume first.";
      console.error("ResumeIQ: resumeAnalysis is missing");
      return;
    }

    if (!selectedFile) {
      reportDownloadStatus.textContent =
        "Please select a resume first.";
      console.error("ResumeIQ: selectedFile is missing");
      return;
    }

    downloadReportButton.disabled = true;
    downloadReportButton.textContent = "Generating PDF...";
    reportDownloadStatus.textContent =
      "Generating your full report...";

    try {
      const payload = {
        resumeAnalysis,
        atsAnalysis,
        skillGapAnalysis,
        careerAnalysis,
        assistantMessages,
        resumeFilename: selectedFile.name
      };

      console.log("ResumeIQ: Sending report request");

      const response = await fetch(
        `${API_URL}/api/report/download`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        }
      );

      console.log(
        "ResumeIQ: Report response",
        response.status,
        response.headers.get("content-type")
      );

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}`;

        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          const text = await response.text();
          if (text) {
            errorMessage = text;
          }
        }

        throw new Error(errorMessage);
      }

      const contentType =
        response.headers.get("content-type") || "";

      if (!contentType.includes("application/pdf")) {
        const text = await response.text();
        throw new Error(
          `Backend did not return a PDF. Response: ${text.substring(0, 300)}`
        );
      }

      const blob = await response.blob();

      if (!blob || blob.size === 0) {
        throw new Error("Generated PDF is empty.");
      }

      console.log(
        "ResumeIQ: PDF received:",
        blob.size,
        "bytes"
      );

      let filename = "ResumeIQ_Report.pdf";
      const disposition = response.headers.get("Content-Disposition") || "";

      if (disposition) {
        const match = disposition.match(/filename="?([^"]+)"?/i);

        if (match && match[1]) {
          filename = match[1];
        }
      }

      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = blobUrl;
      link.download = filename;
      link.style.display = "none";

      document.body.appendChild(link);

      console.log(
        "ResumeIQ: Starting browser download:",
        filename
      );

      link.click();

      document.body.removeChild(link);

      setTimeout(() => {
        window.URL.revokeObjectURL(blobUrl);
      }, 1000);

      reportDownloadStatus.textContent =
        "Report downloaded successfully.";
    } catch (error) {
      console.error(
        "ResumeIQ: Report download failed:",
        error
      );

      reportDownloadStatus.textContent =
        `Report download failed: ${error.message}`;
    } finally {
      downloadReportButton.disabled = false;
      downloadReportButton.textContent =
        "📥 Download Full Report";
    }
  });
}
