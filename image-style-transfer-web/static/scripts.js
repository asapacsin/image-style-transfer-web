const image_input_content = document.querySelector("#content_file");

image_input_content.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image-content").style.backgroundImage = `url(${uploaded_image})`;
  });
  reader.readAsDataURL(this.files[0]);
});

$("img").click(function(){
  $("img").removeClass("selected_image");
  $(this).addClass('selected_image');
  var path = $(this).attr('src');
  document.form.style_file.value = path;
});