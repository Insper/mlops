let longExercises = document.querySelectorAll(".admonition.long textarea");

longExercises.forEach((el) => {
  el.addEventListener("keydown", (evt) => {
    if (evt.keyCode == 9) {
      evt.preventDefault();
      el.setRangeText("    ");
      el.selectionStart += 4;
    }
  });
});

