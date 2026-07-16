document.querySelectorAll("[data-toggle-password]").forEach((button) => {
    button.addEventListener("click", () => {
        const input = document.getElementById(button.dataset.togglePassword);

        if (!input) {
            return;
        }

        input.type = input.type === "password" ? "text" : "password";
    });
});

document.querySelectorAll("[data-auth-form]").forEach((form) => {
    form.addEventListener("submit", () => {
        const submitButton = form.querySelector(".submit-button");

        if (!submitButton) {
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = submitButton.dataset.submittingText || "處理中...";
    });
});

document.querySelectorAll("[data-close-alert]").forEach((button) => {
    button.addEventListener("click", () => {
        button.closest("[data-auth-alert]")?.classList.add("is-hidden");
    });
});
