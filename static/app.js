const checkBtn = document.getElementById("checkBtn");
const usernamesField = document.getElementById("usernames");
const statusText = document.getElementById("statusText");
const resultBody = document.getElementById("resultBody");
const stats = document.getElementById("stats");

const totalCount = document.getElementById("totalCount");
const aliveCount = document.getElementById("aliveCount");
const suspendedCount = document.getElementById("suspendedCount");
const deadCount = document.getElementById("deadCount");
const unknownCount = document.getElementById("unknownCount");

function renderEmpty(message) {
    resultBody.innerHTML = `
        <tr class="empty-row">
            <td colspan="4">${message}</td>
        </tr>
    `;
}

function renderResults(results) {
    resultBody.innerHTML = results.map((item) => `
        <tr>
            <td>@${item.username}</td>
            <td><span class="badge ${item.status}">${item.status}</span></td>
            <td>${item.reason}</td>
            <td><a href="${item.profile_url}" target="_blank" rel="noreferrer">Mở profile</a></td>
        </tr>
    `).join("");
}

function renderSummary(summary) {
    totalCount.textContent = summary.total;
    aliveCount.textContent = summary.alive;
    suspendedCount.textContent = summary.suspended;
    deadCount.textContent = summary.dead;
    unknownCount.textContent = summary.unknown;
    stats.hidden = false;
}

checkBtn.addEventListener("click", async () => {
    const usernames = usernamesField.value.trim();

    if (!usernames) {
        renderEmpty("Hãy nhập ít nhất một username.");
        stats.hidden = true;
        return;
    }

    checkBtn.disabled = true;
    statusText.textContent = "Đang kiểm tra danh sách username...";
    renderEmpty("Đang tải kết quả...");

    try {
        const response = await fetch("/api/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usernames }),
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Không thể kiểm tra username.");
        }

        renderResults(data.results);
        renderSummary(data.summary);
        statusText.textContent = `Hoàn tất ${data.summary.total} username.`;
    } catch (error) {
        renderEmpty(error.message);
        stats.hidden = true;
        statusText.textContent = "Có lỗi xảy ra.";
    } finally {
        checkBtn.disabled = false;
    }
});
