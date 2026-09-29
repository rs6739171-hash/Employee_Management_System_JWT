document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });

        document.addEventListener("click", (event) => {
            if (
                window.innerWidth <= 780 &&
                sidebar.classList.contains("open") &&
                !sidebar.contains(event.target) &&
                !menuToggle.contains(event.target)
            ) {
                sidebar.classList.remove("open");
            }
        });
    }

    const dateTarget = document.getElementById("currentDate");
    if (dateTarget) {
        dateTarget.textContent = new Intl.DateTimeFormat("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }).format(new Date());
    }

    const passwordToggle = document.getElementById("passwordToggle");
    const passwordInput = document.getElementById("password");
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener("click", () => {
            const hidden = passwordInput.type === "password";
            passwordInput.type = hidden ? "text" : "password";
            passwordToggle.textContent = hidden ? "Hide" : "Show";
        });
    }

    const searchInput = document.getElementById("employeeSearch");
    const table = document.getElementById("employeeTable");
    if (searchInput && table) {
        const rows = [...table.querySelectorAll("tbody tr[data-search]")];

        searchInput.addEventListener("input", () => {
            const value = searchInput.value.trim().toLowerCase();
            rows.forEach((row) => {
                const haystack = (row.dataset.search || "").toLowerCase();
                row.style.display = haystack.includes(value) ? "" : "none";
            });
        });
    }

    document.querySelectorAll("[data-delete-name]").forEach((link) => {
        link.addEventListener("click", (event) => {
            const name = link.dataset.deleteName || "this employee";
            if (!window.confirm(`Delete ${name}? This action cannot be undone.`)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll('input[name="phone"]').forEach((input) => {
        input.addEventListener("input", () => {
            input.value = input.value.replace(/[^0-9+ -]/g, "");
        });
    });
});
