document.addEventListener("click", (event) => {
  const clickedMenu = event.target.closest(".nav-dropdown");

  document.querySelectorAll(".nav-dropdown[open]").forEach((menu) => {
    if (menu !== clickedMenu) menu.removeAttribute("open");
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;

  const openMenu = document.querySelector(".nav-dropdown[open]");
  if (!openMenu) return;

  openMenu.removeAttribute("open");
  openMenu.querySelector("summary")?.focus();
});
