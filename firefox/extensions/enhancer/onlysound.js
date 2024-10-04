const myButton = document.createElement("button");
myButton.textContent = "\uf03d"; 
myButton.style.fontFamily = "FontAwesome"; 
myButton.style.fontSize = "16px";
myButton.style.cursor = "pointer";
myButton.style.backgroundColor = "#232323";
myButton.style.color = "#E8E6E3";
myButton.style.borderRadius = "20px";
myButton.style.padding = "12px 15px";
myButton.style.position = "absolute";
myButton.style.border = "none";
myButton.style.top = "8px";
myButton.style.left = "983px";
myButton.style.zIndex = "9000"; 

let isAudioMode = false;
let loadingOverlay;

function showLoading() {
  loadingOverlay = document.createElement("div");
  loadingOverlay.style.position = "fixed";
  loadingOverlay.style.top = "0";
  loadingOverlay.style.left = "0";
  loadingOverlay.style.width = "100%";
  loadingOverlay.style.height = "100%";
  loadingOverlay.style.backgroundColor = "#00000099";
  loadingOverlay.style.zIndex = "9999"; 

  const loadingImage = document.createElement("img");
  loadingImage.src = "https://cdn2.iconfinder.com/data/icons/games-solic/24/Pokeball-1024.png"; 
  loadingImage.style.width = "100px"; 
  loadingImage.style.position = "absolute";
  loadingImage.style.top = "50%";
  loadingImage.style.left = "50%";
  loadingImage.style.transform = "translate(-50%, -50%)"; 

  loadingOverlay.appendChild(loadingImage);
  document.body.appendChild(loadingOverlay);
}

function hideLoading() {
  if (loadingOverlay) {
    loadingOverlay.remove();
  }
}

myButton.addEventListener("click", async function() {
  const video = document.querySelector('video'); 

  if (video) {
    const thumbnail = video.poster; 

    showLoading(); 

    if (!isAudioMode) {
      video.style.display = "none";
      const img = document.createElement("img");
      img.src = thumbnail; 
      img.style.width = "100%"; 
      img.style.display = "block"; 
      img.style.position = "absolute";
      img.style.top = "0"; 
      img.style.left = "0"; 

      const videoContainer = document.querySelector('ytd-player');
      if (videoContainer) {
        videoContainer.appendChild(img); 
      }

      myButton.textContent = "\uf028"; 
      isAudioMode = true; 

      await new Promise(resolve => setTimeout(resolve, 500));
      hideLoading(); 
    } else {
      const img = document.querySelector('img'); 
      if (img) {
        img.remove(); 
      }

      myButton.textContent = "\uf03d"; 
      isAudioMode = false;

      video.style.display = "block"; 
      video.play(); 
      await new Promise(resolve => setTimeout(resolve, 500));
      hideLoading(); 
    }
  } else {
    console.log("not video.");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const video = document.querySelector('video');
  if (video) {
    const thumbnail = video.poster; 
    video.setAttribute('thumbnail', thumbnail); 
  }
});

document.body.appendChild(myButton);
