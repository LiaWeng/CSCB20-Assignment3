function hideMessage() {
  const tohide = document.querySelector(".hide")

  if (tohide) {
    setTimeout(function () {
      tohide.classList.add("hidden")
    }, 3000)
  }
}
