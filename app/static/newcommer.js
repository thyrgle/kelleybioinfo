/**
 * Presents a 
 */
function showNewUserAlert(registerUrl, loginUrl) {
  Swal.fire({
    title: "Welcome!", 
	  html: `Kelley Bio Info is a website for practicing problems related to \
	        bioinformatics. To keep track of your progress, you must either \
          <a href='${registerUrl}'>register</a> or <a href='${loginUrl}'>log in</a>
          `,
    confirmButtonText: "Got it!",
          // Needed to prevent the dialogue from messing up the existing divs.
    heightAuto: false,
  });
}
