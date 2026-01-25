import jsPDF from "jspdf";

export function generatePDF(data) {
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("AI Interview Feedback Report", 20, 20);

  doc.setFontSize(12);
  doc.text(`Score: ${data.score}/10`, 20, 35);
  doc.text("Transcription:", 20, 50);
  doc.text(data.transcript, 20, 60, { maxWidth: 170 });

  doc.text("Feedback:", 20, 120);
  data.feedback.forEach((f, i) => {
    doc.text(`• ${f}`, 20, 130 + i * 8);
  });

  doc.save("Interview_Feedback_Report.pdf");
}
