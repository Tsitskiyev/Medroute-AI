import React, { useMemo, useState } from "react";

type UrgencyLevel = "Normal" | "Urgent" | "Emergency";

type TriageResponse = {
  possible_conditions: string[];
  recommended_specialist: string;
  urgency_level: UrgencyLevel;
  disclaimer: string;
  detected_symptoms: string[];
  explanation: string;
};

type XRayResponse = {
  error: string | null;
  is_pneumonia: boolean | null;
  confidence: number | null;
  class_label: string | null;
  confidence_percent: number | null;
};

const palette = {
  bg: "#f2f6f9",
  shell: "#eef3f7",
  panel: "#ffffff",
  panelSoft: "#f7fafc",
  border: "#d8e3ea",
  borderStrong: "#c7d5df",
  text: "#19384d",
  textSoft: "#5f7b8f",
  textMuted: "#7a92a3",
  primary: "#2f6d94",
  primarySoft: "#e8f1f7",
  successBg: "#eaf7ef",
  successText: "#1f7a43",
  successBorder: "#bfdfca",
  warningBg: "#fff6e3",
  warningText: "#9b6500",
  warningBorder: "#eed59c",
  dangerBg: "#fdecec",
  dangerText: "#b42318",
  dangerBorder: "#efbeb9",
  disclaimerBg: "#fff9eb",
  disclaimerText: "#7b5a1d",
  disclaimerBorder: "#e8d8a1",
};

const pageStyle: React.CSSProperties = {
  minHeight: "100vh",
  background: palette.bg,
  color: palette.text,
  fontFamily:
    "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
};

const shellStyle: React.CSSProperties = {
  maxWidth: 1380,
  margin: "0 auto",
  padding: "18px 18px 28px",
  boxSizing: "border-box",
};

const topBarStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1fr auto",
  gap: 16,
  alignItems: "center",
  background: palette.panel,
  border: `1px solid ${palette.border}`,
  borderRadius: 18,
  padding: "16px 20px",
  boxShadow: "0 8px 24px rgba(15, 23, 42, 0.04)",
  marginBottom: 18,
};

const brandWrapStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 14,
};

const emblemStyle: React.CSSProperties = {
  width: 54,
  height: 54,
  borderRadius: 16,
  background: palette.primarySoft,
  border: `1px solid ${palette.border}`,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 24,
};

const topTitleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 24,
  fontWeight: 800,
  color: palette.text,
};

const topSubtitleStyle: React.CSSProperties = {
  margin: "4px 0 0 0",
  fontSize: 14,
  color: palette.textSoft,
};

const statusChipStyle: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 999,
  background: palette.panelSoft,
  border: `1px solid ${palette.border}`,
  color: palette.textSoft,
  fontWeight: 700,
  fontSize: 13,
};

const workspaceStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "290px minmax(0, 1fr)",
  gap: 18,
  alignItems: "start",
};

const cardStyle: React.CSSProperties = {
  background: palette.panel,
  border: `1px solid ${palette.border}`,
  borderRadius: 20,
  boxShadow: "0 10px 24px rgba(15, 23, 42, 0.04)",
};

const panelStyle: React.CSSProperties = {
  ...cardStyle,
  padding: 25,
};

const sidebarStyle: React.CSSProperties = {
  display: "grid",
  gap: 18,
};

const mainStyle: React.CSSProperties = {
  display: "grid",
  gap: 18,
};

const sectionTitleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 18,
  fontWeight: 800,
  color: palette.text,
};

const sectionSubtitleStyle: React.CSSProperties = {
  margin: "8px 0 0 0",
  fontSize: 14,
  color: palette.textSoft,
  lineHeight: 1.6,
};

const mutedTextStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 14,
  color: palette.textSoft,
  lineHeight: 1.6,
};

const labelStyle: React.CSSProperties = {
  display: "block",
  marginBottom: 8,
  fontSize: 14,
  fontWeight: 700,
  color: "#2b4b60",
};

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: 190,
  resize: "vertical",
  boxSizing: "border-box",
  padding: 16,
  borderRadius: 16,
  border: `1px solid ${palette.borderStrong}`,
  background: "#fcfeff",
  color: palette.text,
  fontSize: 15,
  lineHeight: 1.6,
  outline: "none",
};

const helperTextStyle: React.CSSProperties = {
  margin: "10px 0 0 0",
  fontSize: 13,
  color: palette.textMuted,
};

const buttonRowStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: 10,
  marginTop: 18,
};

const primaryButtonStyle: React.CSSProperties = {
  border: "none",
  borderRadius: 14,
  background: palette.primary,
  color: "#ffffff",
  padding: "12px 18px",
  fontSize: 15,
  fontWeight: 700,
  cursor: "pointer",
};

const secondaryButtonStyle: React.CSSProperties = {
  border: `1px solid ${palette.borderStrong}`,
  borderRadius: 14,
  background: "#ffffff",
  color: "#35586f",
  padding: "12px 18px",
  fontSize: 15,
  fontWeight: 600,
  cursor: "pointer",
};

const softPanelStyle: React.CSSProperties = {
  background: palette.panelSoft,
  border: `1px solid ${palette.border}`,
  borderRadius: 16,
  padding: 14,
};

const infoTitleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 15,
  fontWeight: 800,
  color: "#28475d",
};

const bodyTextStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 15,
  lineHeight: 1.7,
  color: "#3d5b6f",
};

const listStyle: React.CSSProperties = {
  margin: "10px 0 0 0",
  paddingLeft: 18,
  fontSize: 15,
  lineHeight: 1.7,
  color: "#3d5b6f",
};

const patientHeaderStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 14,
  marginBottom: 14,
};

const avatarStyle: React.CSSProperties = {
  width: 58,
  height: 58,
  borderRadius: 18,
  background: palette.primarySoft,
  border: `1px solid ${palette.border}`,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 24,
};

const patientNameStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 17,
  fontWeight: 800,
  color: palette.text,
};

const patientMetaStyle: React.CSSProperties = {
  margin: "4px 0 0 0",
  fontSize: 13,
  color: palette.textMuted,
};

const miniGridStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 10,
};

const miniCardStyle: React.CSSProperties = {
  background: "#fcfeff",
  border: `1px solid ${palette.border}`,
  borderRadius: 14,
  padding: 12,
};

const miniLabelStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 12,
  color: palette.textMuted,
};

const miniValueStyle: React.CSSProperties = {
  margin: "6px 0 0 0",
  fontSize: 14,
  fontWeight: 700,
  color: palette.text,
};

const caseStripStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1.2fr repeat(4, minmax(140px, 1fr))",
  gap: 12,
  alignItems: "stretch",
};

const stripLeadCardStyle: React.CSSProperties = {
  ...cardStyle,
  padding: 18,
  background: palette.panelSoft,
};

const stripCardStyle: React.CSSProperties = {
  ...cardStyle,
  padding: 16,
  background: "#fcfeff",
};

const stripLabelStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 12,
  color: palette.textMuted,
};

const stripValueStyle: React.CSSProperties = {
  margin: "8px 0 0 0",
  fontSize: 18,
  fontWeight: 800,
  color: palette.text,
};

const workspaceGridStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1.05fr 0.95fr",
  gap: 16,
};

const blockStyle: React.CSSProperties = {
  background: "#fbfdff",
  border: `1px solid ${palette.border}`,
  borderRadius: 16,
  padding: 16,
};

const chipWrapStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: 10,
};

const chipStyle: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: 999,
  background: palette.primarySoft,
  border: `1px solid ${palette.border}`,
  color: "#2c607d",
  fontSize: 13,
  fontWeight: 700,
};

const emptyStateStyle: React.CSSProperties = {
  padding: 22,
  borderRadius: 16,
  border: `1px dashed ${palette.borderStrong}`,
  background: palette.panelSoft,
};

const footerNoteStyle: React.CSSProperties = {
  marginTop: 8,
  fontSize: 12,
  color: palette.textMuted,
  lineHeight: 1.6,
};

const xrayPreviewStyle: React.CSSProperties = {
  width: "100%",
  maxHeight: 180,
  objectFit: "cover",
  borderRadius: 14,
  border: `1px solid ${palette.borderStrong}`,
  marginTop: 12,
};

const dangerTextBlockStyle: React.CSSProperties = {
  marginTop: 18,
  padding: 14,
  borderRadius: 14,
  background: palette.dangerBg,
  border: `1px solid ${palette.dangerBorder}`,
  color: palette.dangerText,
  fontWeight: 600,
};

function getUrgencyStyles(
  level: UrgencyLevel
): { bg: string; text: string; border: string } {
  switch (level) {
    case "Normal":
      return {
        bg: palette.successBg,
        text: palette.successText,
        border: palette.successBorder,
      };
    case "Urgent":
      return {
        bg: palette.warningBg,
        text: palette.warningText,
        border: palette.warningBorder,
      };
    case "Emergency":
      return {
        bg: palette.dangerBg,
        text: palette.dangerText,
        border: palette.dangerBorder,
      };
    default:
      return {
        bg: palette.panelSoft,
        text: palette.textSoft,
        border: palette.border,
      };
  }
}

function createUrgencyBadgeStyle(level: UrgencyLevel): React.CSSProperties {
  const s = getUrgencyStyles(level);

  return {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "8px 14px",
    borderRadius: 999,
    background: s.bg,
    color: s.text,
    border: `1px solid ${s.border}`,
    fontSize: 13,
    fontWeight: 800,
  };
}

function createXrayStatusBadgeStyle(isPneumonia: boolean | null): React.CSSProperties {
  if (isPneumonia === null) {
    return {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "8px 14px",
      borderRadius: 999,
      background: palette.panelSoft,
      color: palette.textSoft,
      border: `1px solid ${palette.border}`,
      fontSize: 13,
      fontWeight: 800,
    };
  }

  return {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "8px 14px",
    borderRadius: 999,
    background: isPneumonia ? palette.dangerBg : palette.successBg,
    color: isPneumonia ? palette.dangerText : palette.successText,
    border: `1px solid ${isPneumonia ? palette.dangerBorder : palette.successBorder}`,
    fontSize: 13,
    fontWeight: 800,
  };
}

function splitSymptoms(input: string): string[] {
  return input
    .split(/[,;\n]/g)
    .map((item) => item.trim())
    .filter(Boolean);
}

function formatTimestamp(): string {
  return new Date().toLocaleString();
}

export default function App() {
  const [input, setInput] = useState("");
  const [data, setData] = useState<TriageResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [timestamp, setTimestamp] = useState("");

  const [xrayFile, setXrayFile] = useState<File | null>(null);
  const [xrayPreview, setXrayPreview] = useState("");
  const [xrayResult, setXrayResult] = useState<XRayResponse | null>(null);
  const [xrayLoading, setXrayLoading] = useState(false);
  const [xrayError, setXrayError] = useState("");

  const parsedCount = useMemo(() => splitSymptoms(input).length, [input]);

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const symptoms = splitSymptoms(input);

      if (symptoms.length === 0) {
        throw new Error("Please enter at least one symptom.");
      }

      const response = await fetch("http://127.0.0.1:8000/triage", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symptoms }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const result: TriageResponse = await response.json();
      setData(result);
      setTimestamp(formatTimestamp());
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to analyze symptoms.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadExample = () => {
    setInput("chest pain, shortness of breath, palpitations");
    setData(null);
    setError("");
  };

  const handleClear = () => {
    setInput("");
    setData(null);
    setError("");
    setTimestamp("");
  };

  const handleXrayFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setXrayFile(file);
    setXrayError("");
    setXrayResult(null);

    if (file) {
      const previewUrl = URL.createObjectURL(file);
      setXrayPreview(previewUrl);
    } else {
      setXrayPreview("");
    }
  };

  const handleAnalyzeXray = async () => {
    if (!xrayFile) {
      setXrayError("Please select an X-Ray image first.");
      return;
    }

    setXrayLoading(true);
    setXrayError("");
    setXrayResult(null);

    try {
      const formData = new FormData();
      formData.append("file", xrayFile);

      const response = await fetch("http://127.0.0.1:8000/analyze-xray", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const result = await response.json();
      setXrayResult({
        error: result.error ?? null,
        is_pneumonia: result.is_pneumonia ?? null,
        confidence: result.confidence ?? null,
        class_label: result.class ?? null,
        confidence_percent: result.confidence_percent ?? null,
      });
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to analyze X-Ray image.";
      setXrayError(message);
    } finally {
      setXrayLoading(false);
    }
  };

  const handleClearXray = () => {
    setXrayFile(null);
    setXrayPreview("");
    setXrayError("");
    setXrayResult(null);
  };

  return (
    <main style={pageStyle}>
      <div style={shellStyle}>
        <header style={topBarStyle}>
          <div style={brandWrapStyle}>
            <div style={emblemStyle}>🩺</div>
            <div>
              <h1 style={topTitleStyle}>MedRoute AI</h1>
              <p style={topSubtitleStyle}>
                Clinical triage and referral workstation
              </p>
            </div>
          </div>

          <div style={statusChipStyle}>Educational non-diagnostic system</div>
        </header>

        <section style={workspaceStyle}>
          <aside style={sidebarStyle}>
            <div style={panelStyle}>
              <div style={patientHeaderStyle}>
                <div style={avatarStyle}>👤</div>
                <div>
                  <h2 style={patientNameStyle}>Patient Intake Case</h2>
                  <p style={patientMetaStyle}>Case ID: MR-AI-DEMO-001</p>
                </div>
              </div>

              <div style={miniGridStyle}>
                <div style={miniCardStyle}>
                  <p style={miniLabelStyle}>Department</p>
                  <p style={miniValueStyle}>General Triage</p>
                </div>
                <div style={miniCardStyle}>
                  <p style={miniLabelStyle}>Mode</p>
                  <p style={miniValueStyle}>Hybrid Rules</p>
                </div>
                <div style={miniCardStyle}>
                  <p style={miniLabelStyle}>Language</p>
                  <p style={miniValueStyle}>EN / RU</p>
                </div>
                <div style={miniCardStyle}>
                  <p style={miniLabelStyle}>Session</p>
                  <p style={miniValueStyle}>Active</p>
                </div>
              </div>
            </div>

            <div style={panelStyle}>
              <h2 style={sectionTitleStyle}>Symptom Intake</h2>
              <p style={sectionSubtitleStyle}>
                Enter symptom items separated by commas, semicolons, or new lines.
              </p>

              <label htmlFor="symptoms" style={labelStyle}>
                Patient-reported symptoms
              </label>

              <textarea
                id="symptoms"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder={
                  "Examples:\nchest pain, shortness of breath, palpitations\n\nили:\nболь в груди\nодышка\nсердцебиение"
                }
                style={textareaStyle}
              />

              <p style={helperTextStyle}>
                Parsed symptom tokens: <strong>{parsedCount}</strong>
              </p>

              <div style={buttonRowStyle}>
                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={loading}
                  style={{
                    ...primaryButtonStyle,
                    opacity: loading ? 0.75 : 1,
                    cursor: loading ? "not-allowed" : "pointer",
                  }}
                >
                  {loading ? "Running..." : "Run Assessment"}
                </button>

                <button
                  type="button"
                  onClick={handleLoadExample}
                  style={secondaryButtonStyle}
                >
                  Load Example
                </button>

                <button
                  type="button"
                  onClick={handleClear}
                  style={secondaryButtonStyle}
                >
                  Clear
                </button>
              </div>

              {error && (
                <div
                  style={{
                    marginTop: 18,
                    padding: 14,
                    borderRadius: 14,
                    background: palette.dangerBg,
                    border: `1px solid ${palette.dangerBorder}`,
                    color: palette.dangerText,
                    fontWeight: 600,
                  }}
                >
                  {error}
                </div>
              )}
            </div>

            <div style={panelStyle}>
              <h2 style={sectionTitleStyle}>Chest X-Ray Upload</h2>
              <p style={sectionSubtitleStyle}>
                Upload a frontal chest X-Ray image for pneumonia screening.
              </p>

              <label htmlFor="xray-file" style={labelStyle}>
                Select X-Ray image
              </label>
              <input
                id="xray-file"
                type="file"
                accept="image/*"
                onChange={handleXrayFileChange}
                style={{
                  width: "100%",
                  padding: "12px 0px",
                  borderRadius: 14,
                  border: `1px solid ${palette.borderStrong}`,
                  background: "#fcfeff",
                  color: palette.text,
                  fontSize: 14,
                }}
              />

              {xrayPreview && (
                <img
                  src={xrayPreview}
                  alt="X-Ray preview"
                  style={xrayPreviewStyle}
                />
              )}

              <div style={buttonRowStyle}>
                <button
                  type="button"
                  onClick={handleAnalyzeXray}
                  disabled={xrayLoading}
                  style={{
                    ...primaryButtonStyle,
                    opacity: xrayLoading ? 0.75 : 1,
                    cursor: xrayLoading ? "not-allowed" : "pointer",
                  }}
                >
                  {xrayLoading ? "Analyzing..." : "Analyze X-Ray"}
                </button>

                <button
                  type="button"
                  onClick={handleClearXray}
                  style={secondaryButtonStyle}
                >
                  Clear Image
                </button>
              </div>

              {xrayError && (
                <div style={dangerTextBlockStyle}>{xrayError}</div>
              )}

              <p style={helperTextStyle}>
                Supported formats: JPG, PNG, BMP. The model is for screening only.
              </p>
            </div>

            <div style={panelStyle}>
              <h2 style={sectionTitleStyle}>Suggested Cases</h2>
              <ul style={listStyle}>
                <li>chest pain, shortness of breath</li>
                <li>rash, itching</li>
                <li>headache, speech difficulty, one-sided weakness</li>
                <li>боль в груди, одышка</li>
              </ul>
            </div>
          </aside>

          <section style={mainStyle}>
            <div style={caseStripStyle}>
              <div style={stripLeadCardStyle}>
                <p style={stripLabelStyle}>Assessment Workspace</p>
                <p style={{ ...stripValueStyle, fontSize: 20 }}>
                  Clinical Decision Support Panel
                </p>
                <p style={{ ...mutedTextStyle, marginTop: 8 }}>
                  {timestamp
                    ? `Last generated: ${timestamp}`
                    : "Awaiting new assessment"}
                </p>
              </div>

              <div style={stripCardStyle}>
                <p style={stripLabelStyle}>Urgency</p>
                <p style={stripValueStyle}>
                  {data ? data.urgency_level : "—"}
                </p>
              </div>

              <div style={stripCardStyle}>
                <p style={stripLabelStyle}>Referral</p>
                <p style={stripValueStyle}>
                  {data ? data.recommended_specialist : "—"}
                </p>
              </div>

              <div style={stripCardStyle}>
                <p style={stripLabelStyle}>Symptoms</p>
                <p style={stripValueStyle}>
                  {data ? data.detected_symptoms.length : 0}
                </p>
              </div>

              <div style={stripCardStyle}>
                <p style={stripLabelStyle}>Conditions</p>
                <p style={stripValueStyle}>
                  {data ? data.possible_conditions.length : 0}
                </p>
              </div>
            </div>

            <div style={panelStyle}>
              {!data && !loading && (
                <div style={emptyStateStyle}>
                  <h2 style={sectionTitleStyle}>No Active Assessment</h2>
                  <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                    Submit symptoms from the intake panel to generate triage
                    classification, specialist routing, candidate conditions,
                    and explanation output.
                  </p>
                </div>
              )}

              {loading && (
                <div style={emptyStateStyle}>
                  <h2 style={sectionTitleStyle}>Assessment in Progress</h2>
                  <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                    Running normalization, rule matching, triage classification,
                    referral mapping, and explanation generation...
                  </p>
                </div>
              )}

              {data && (
                <div style={workspaceGridStyle}>
                  <div style={{ display: "grid", gap: 16 }}>
                    <div style={blockStyle}>
                      <h3 style={infoTitleStyle}>Triage Status</h3>
                      <div style={{ marginTop: 12 }}>
                        <span style={createUrgencyBadgeStyle(data.urgency_level)}>
                          {data.urgency_level}
                        </span>
                      </div>
                      <p style={{ ...bodyTextStyle, marginTop: 12 }}>
                        The system classified the case using rule-based urgency
                        logic combined with normalized symptom patterns.
                      </p>
                    </div>

                    <div style={blockStyle}>
                      <h3 style={infoTitleStyle}>Detected Symptoms</h3>
                      <div style={{ marginTop: 12, ...chipWrapStyle }}>
                        {data.detected_symptoms.map((symptom) => (
                          <span key={symptom} style={chipStyle}>
                            {symptom}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div style={blockStyle}>
                      <h3 style={infoTitleStyle}>Explainable Reasoning</h3>
                      <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                        {data.explanation}
                      </p>
                    </div>
                  </div>

                  <div style={{ display: "grid", gap: 16 }}>
                    <div style={blockStyle}>
                      <h3 style={infoTitleStyle}>Referral Recommendation</h3>
                      <p style={{ ...stripValueStyle, marginTop: 10 }}>
                        {data.recommended_specialist}
                      </p>
                      <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                        Routing is based on symptom-to-specialist mapping from the
                        knowledge base.
                      </p>
                    </div>

                    <div style={blockStyle}>
                      <h3 style={infoTitleStyle}>Candidate Conditions</h3>
                      <ul style={listStyle}>
                        {data.possible_conditions.map((condition) => (
                          <li key={condition}>{condition}</li>
                        ))}
                      </ul>
                    </div>

                    <div
                      style={{
                        ...blockStyle,
                        background: palette.disclaimerBg,
                        border: `1px solid ${palette.disclaimerBorder}`,
                      }}
                    >
                      <h3
                        style={{
                          ...infoTitleStyle,
                          color: palette.disclaimerText,
                        }}
                      >
                        Medical Disclaimer
                      </h3>
                      <p
                        style={{
                          ...bodyTextStyle,
                          marginTop: 10,
                          color: palette.disclaimerText,
                        }}
                      >
                        {data.disclaimer}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div style={panelStyle}>
              <h2 style={sectionTitleStyle}>Chest X-Ray Result</h2>
              {!xrayResult && !xrayLoading && (
                <div style={emptyStateStyle}>
                  <h2 style={sectionTitleStyle}>No X-Ray Analysis</h2>
                  <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                    Upload an image to receive a pneumonia screening result
                    and confidence score.
                  </p>
                </div>
              )}

              {xrayLoading && (
                <div style={emptyStateStyle}>
                  <h2 style={sectionTitleStyle}>Analyzing X-Ray</h2>
                  <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                    The model is processing the image and generating a pneumonia
                    score.
                  </p>
                </div>
              )}

              {xrayResult && !xrayResult.error && (
                <div style={workspaceGridStyle}>
                  <div style={blockStyle}>
                    <h3 style={infoTitleStyle}>Prediction</h3>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", marginTop: 10 }}>
                      <span style={createXrayStatusBadgeStyle(xrayResult.is_pneumonia)}>
                        {xrayResult.is_pneumonia === true
                          ? "Pneumonia"
                          : xrayResult.is_pneumonia === false
                          ? "Normal"
                          : "Unknown"}
                      </span>
                      <p style={{ ...bodyTextStyle, margin: 0 }}>
                        {xrayResult.class_label ?? "No label"}
                      </p>
                    </div>
                    <p style={{ ...bodyTextStyle, marginTop: 14 }}>
                      Confidence: {xrayResult.confidence_percent?.toFixed(1) ?? "—"}%
                    </p>
                  </div>

                  <div style={blockStyle}>
                    <h3 style={infoTitleStyle}>Interpretation</h3>
                    <p style={{ ...bodyTextStyle, marginTop: 10 }}>
                      {xrayResult.is_pneumonia === true
                        ? "Detection suggests pneumonia features are present."
                        : xrayResult.is_pneumonia === false
                        ? "The X-Ray appears more consistent with a normal chest image."
                        : "No definitive finding could be produced."}
                    </p>
                  </div>
                </div>
              )}

              {xrayResult && xrayResult.error && (
                <div style={dangerTextBlockStyle}>{xrayResult.error}</div>
              )}
            </div>

            <div style={panelStyle}>
              <h2 style={sectionTitleStyle}>System Overview</h2>
              <div style={{ marginTop: 12, display: "grid", gap: 14 }}>
                <div style={softPanelStyle}>
                  <h3 style={infoTitleStyle}>Clinical Logic</h3>
                  <p style={{ ...bodyTextStyle, marginTop: 8 }}>
                    Safety-aware rule engine for urgency classification and
                    specialist recommendation.
                  </p>
                </div>

                <div style={softPanelStyle}>
                  <h3 style={infoTitleStyle}>Multilingual Intake</h3>
                  <p style={{ ...bodyTextStyle, marginTop: 8 }}>
                    Symptom normalization supports both English and Russian input.
                  </p>
                </div>

                <div style={softPanelStyle}>
                  <h3 style={infoTitleStyle}>Portfolio Positioning</h3>
                  <p style={{ ...bodyTextStyle, marginTop: 8 }}>
                    Explainable clinical routing assistant with hybrid AI
                    architecture and non-diagnostic safety boundaries.
                  </p>
                </div>
              </div>

              <p style={footerNoteStyle}>
                Suggested framing for presentation: AI-assisted clinical triage
                workstation for multilingual symptom intake, urgency assessment,
                and specialist referral support.
              </p>
            </div>
          </section>
        </section>
      </div>
    </main>
  );
}