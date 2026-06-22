(function () {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const browseBtn = document.getElementById("browse-btn");
    const fileInfo = document.getElementById("file-info");
    const fileName = document.getElementById("file-name");
    const removeFileBtn = document.getElementById("remove-file-btn");
    const form = document.getElementById("upload-form");
    const projectName = document.getElementById("project-name");
    const contextInput = document.getElementById("context");
    const codeInput = document.getElementById("code");
    const testsInput = document.getElementById("tests");
    const submitBtn = document.getElementById("submit-btn");
    const overlay = document.getElementById("validation-overlay");
    const overlayLoading = document.getElementById("overlay-loading");
    const overlaySuccess = document.getElementById("overlay-success");
    const overlayGenerating = document.getElementById("overlay-generating");
    const overlayGenerated = document.getElementById("overlay-generated");
    const overlayError = document.getElementById("overlay-error");
    const overlayErrors = document.getElementById("overlay-errors");
    const generateTestsBtn = document.getElementById("generate-tests-btn");
    const retryBtn = document.getElementById("retry-btn");
    const testCodeContent = document.getElementById("test-code-content");
    const copyCodeBtn = document.getElementById("copy-code-btn");
    const closeOverlayBtn = document.getElementById("close-overlay-btn");

    let selectedFile = null;
    let sessionId = null;

    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : null;
    }

    sessionId = getCookie("session_id");

    function updateSubmitState() {
        submitBtn.disabled = !(selectedFile && projectName.value.trim() && contextInput.value.trim() && codeInput.value.trim() && testsInput.value.trim());
    }

    function showFile(file) {
        selectedFile = file;
        fileName.textContent = file.name;
        fileInfo.classList.remove("hidden");
        document.querySelector(".drop-zone-text").style.display = "none";
        document.querySelector(".drop-zone-or").style.display = "none";
        browseBtn.style.display = "none";
        const nameWithoutExt = file.name.replace(/\.py$/i, "");
        projectName.value = nameWithoutExt;
        updateSubmitState();
    }

    function clearFile() {
        selectedFile = null;
        fileInfo.classList.add("hidden");
        document.querySelector(".drop-zone-text").style.display = "block";
        document.querySelector(".drop-zone-or").style.display = "block";
        browseBtn.style.display = "inline-block";
        fileInput.value = "";
        projectName.value = "";
        updateSubmitState();
    }

    function showOverlay(state) {
        overlay.classList.remove("hidden");
        overlayLoading.classList.add("hidden");
        overlaySuccess.classList.add("hidden");
        overlayGenerating.classList.add("hidden");
        overlayGenerated.classList.add("hidden");
        overlayError.classList.add("hidden");
        if (state === "loading") overlayLoading.classList.remove("hidden");
        else if (state === "success") overlaySuccess.classList.remove("hidden");
        else if (state === "generating") overlayGenerating.classList.remove("hidden");
        else if (state === "generated") overlayGenerated.classList.remove("hidden");
        else if (state === "error") overlayError.classList.remove("hidden");
    }

    function hideOverlay() {
        overlay.classList.add("hidden");
    }

    function showOverlaySuccess(data) {
        showOverlay("success");
    }

    function showOverlayError(data) {
        const errors = data.errors || [data.detail || "Error desconocido"];
        const list = errors.map(function (e) {
            if (typeof e === "string") return "<li>" + e + "</li>";
            return "<li>L\u00ednea " + (e.line || "?") + ": " + e.message + "</li>";
        }).join("");
        overlayErrors.innerHTML = "<ul>" + list + "</ul>";
        showOverlay("error");
    }

    dropZone.addEventListener("dragenter", function (e) {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragover", function (e) {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", function () {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", function (e) {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const f = files[0];
            if (!f.name.endsWith(".py")) {
                showOverlayError({ errors: ["Solo se permiten archivos .py"] });
                return;
            }
            showFile(f);
        }
    });

    browseBtn.addEventListener("click", function () {
        fileInput.click();
    });

    dropZone.addEventListener("click", function (e) {
        if (e.target === dropZone || e.target.closest(".drop-zone-text") || e.target.closest(".drop-zone-or")) {
            if (!selectedFile) fileInput.click();
        }
    });

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            showFile(fileInput.files[0]);
        }
    });

    removeFileBtn.addEventListener("click", function () {
        clearFile();
    });

    projectName.addEventListener("input", updateSubmitState);
    contextInput.addEventListener("input", updateSubmitState);
    codeInput.addEventListener("input", updateSubmitState);
    testsInput.addEventListener("input", updateSubmitState);

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!selectedFile) return;

        submitBtn.disabled = true;
        submitBtn.textContent = "Subiendo...";
        showOverlay("loading");

        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("project_name", projectName.value.trim());
        const combinedPrompt = "Contexto:\n" + contextInput.value.trim() + "\n\nCódigo:\n" + codeInput.value.trim() + "\n\nPruebas:\n" + testsInput.value.trim();
        formData.append("prompt", combinedPrompt);

        try {
            const response = await fetch("/api/v1/upload/source", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                sessionId = data.sessionId;
                showOverlaySuccess(data);
            } else {
                showOverlayError(data);
            }
        } catch (err) {
            showOverlayError({ errors: ["Error de conexión con el servidor"] });
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Subir y validar";
        }
    });

    generateTestsBtn.addEventListener("click", async function () {
        const context = contextInput.value.trim();
        const code = codeInput.value.trim();
        const tests = testsInput.value.trim();
        const combinedPrompt = "Contexto:\n" + context + "\n\nCódigo:\n" + code + "\n\nPruebas:\n" + tests;

        showOverlay("generating");

        try {
            const response = await fetch("/api/v1/ai/generate-tests", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId, prompt: combinedPrompt }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                testCodeContent.textContent = data.test_code;
                showOverlay("generated");
            } else {
                showOverlayError({ errors: [data.error || "Error al generar pruebas"] });
            }
        } catch (err) {
            showOverlayError({ errors: ["Error de conexión con el servidor"] });
        }
    });

    copyCodeBtn.addEventListener("click", function () {
        navigator.clipboard.writeText(testCodeContent.textContent).then(function () {
            copyCodeBtn.textContent = "Copiado!";
            setTimeout(function () { copyCodeBtn.textContent = "Copiar código"; }, 2000);
        });
    });

    closeOverlayBtn.addEventListener("click", function () {
        hideOverlay();
    });

    retryBtn.addEventListener("click", function () {
        hideOverlay();
        clearFile();
    });

    window.addEventListener("beforeunload", function () {
        if (sessionId) {
            navigator.sendBeacon("/api/v1/upload/source/" + sessionId);
        }
    });
})();
