const startGameButton = document.querySelector("#startGameButton");
const gameStatus = document.querySelector("#gameStatus");

document.querySelectorAll(".nav-item").forEach((item) => {
    item.addEventListener("pointerenter", () => {
        document.activeElement?.blur?.();
    });
});

startGameButton?.addEventListener("click", () => {
    if (!gameStatus) {
        return;
    }

    gameStatus.textContent = "目前狀態：正在尋找合適的對局...";
});
