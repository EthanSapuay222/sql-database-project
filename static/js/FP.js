// Para sa submission report button
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
import {
  getAuth,
  signInAnonymously,
  signInWithCustomToken,
  onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
import {
  getFirestore,
  collection,
  addDoc,
  serverTimestamp,
} from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

const appId = typeof __app_id !== "undefined" ? __app_id : "default-app-id";
const firebaseConfig =
  typeof __firebase_config !== "undefined"
    ? JSON.parse(__firebase_config)
    : null;
const initialAuthToken =
  typeof __initial_auth_token !== "undefined" ? __initial_auth_token : null;

let app, db, auth;
let userId = null;
let isAuthReady = false;

const reportForm = document.getElementById("report-form");
const messageBox = document.getElementById("message-box");
const userIdDisplay = document.getElementById("user-id-display");

function showMessage(message, isSuccess) {
  messageBox.textContent = message;
  messageBox.classList.remove(
    "hidden",
    "bg-red-100",
    "text-red-700",
    "bg-green-100",
    "text-green-700"
  );

  if (isSuccess) {
    messageBox.classList.add("bg-green-100", "text-green-700");
  } else {
    messageBox.classList.add("bg-red-100", "text-red-700");
  }
  setTimeout(() => {
    messageBox.classList.add("hidden");
  }, 5000);
}

if (firebaseConfig) {
  app = initializeApp(firebaseConfig);
  db = getFirestore(app);
  auth = getAuth(app);

  onAuthStateChanged(auth, async (user) => {
    if (user) {
      userId = user.uid;
      isAuthReady = true;
      userIdDisplay.innerHTML = `<span class="font-bold">User ID:</span> ${userId}`;
    } else {
      userIdDisplay.innerHTML = `<span class="font-bold">Status:</span> Signing in...`;
      try {
        if (initialAuthToken) {
          await signInWithCustomToken(auth, initialAuthToken);
        } else {
          await signInAnonymously(auth);
        }
      } catch (error) {
        console.error("Authentication failed:", error);
        userIdDisplay.innerHTML = `<span class="font-bold">Error:</span> Auth failed.`;
        isAuthReady = true;
      }
    }
  });
} else {
  console.error("Firebase configuration is missing.");
  userIdDisplay.innerHTML = `<span class="font-bold">Error:</span> Config missing. Data saving disabled.`;
  isAuthReady = true;
}

reportForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!isAuthReady || !userId) {
    showMessage("Authentication not ready. Please wait a moment.", false);
    return;
  }

  const formData = new FormData(reportForm);
  const reportData = {
    title: formData.get("report-title"),
    description: formData.get("description"),
    category: formData.get("category"),
    location: formData.get("location"),
    severity: formData.get("severity"),
    timestamp: serverTimestamp(),
    reportedBy: userId,
  };

  const submitButton = reportForm.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Submitting...";

  try {
    const reportCollectionPath = `artifacts/${appId}/users/${userId}/reports`;
    const colRef = collection(db, reportCollectionPath);
    await addDoc(colRef, reportData);

    showMessage("Report submitted successfully!", true);
    reportForm.reset();
  } catch (error) {
    console.error("Error submitting report:", error);
    showMessage(`Error: Could not submit report. ${error.message}`, false);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Submit Report";
  }
});
//Para to sa Dashboard
