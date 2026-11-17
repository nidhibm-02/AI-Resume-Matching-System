
const API_BASE_URL = "https://ai-resume-matching-api.onrender.com";

export async function matchResumes(jobDescription, files) {
  const formData = new FormData();

  formData.append("job_description", jobDescription);

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(
    `${API_BASE_URL}/match-resumes`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Matching failed");
  }

  return await response.json();
}
