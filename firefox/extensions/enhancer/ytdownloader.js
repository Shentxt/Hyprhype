const myButton = document.createElement("button");
myButton.textContent = "\uf019";
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

let isPopupOpen = false;
let popupContainer;
let backgroundBlur;

function togglePopup() {
  if (isPopupOpen) {
    document.body.removeChild(popupContainer);
    document.body.removeChild(backgroundBlur);
   // myButton.style.display = "block"; 
    isPopupOpen = false;
  } else {
    const iframe = document.createElement("iframe");
    iframe.src = "https://yt1s.com.co/en27/";
    iframe.style.width = "650px";
    iframe.style.height = "450px";
    iframe.style.border = "solid";
    iframe.style.borderRadius = "12px";

    popupContainer = document.createElement("div");
    popupContainer.style.position = "fixed";
    popupContainer.style.bottom = "60px";
    popupContainer.style.right = "300px";
    popupContainer.style.zIndex = "9999"; 
    popupContainer.appendChild(iframe);

    const closeButton = document.createElement("button");
    closeButton.textContent = "X";
    closeButton.style.position = "absolute";
    closeButton.style.top = "20px";
    closeButton.style.right = "10px";
    closeButton.style.padding = "5px";
    closeButton.style.border = "none";
    closeButton.style.backgroundColor = "transparent";
    closeButton.style.color = "#c0caf5";
    closeButton.style.cursor = "pointer";
    closeButton.addEventListener("click", togglePopup);
    popupContainer.appendChild(closeButton);

    backgroundBlur = document.createElement("div"); 
    backgroundBlur.style.position = "fixed";
    backgroundBlur.style.top = "0";
    backgroundBlur.style.left = "0";
    backgroundBlur.style.width = "100%";
    backgroundBlur.style.height = "100%";
    backgroundBlur.style.backgroundColor = "#2e344099";
    backgroundBlur.style.backdropFilter = "blur(5px)"; 
    backgroundBlur.style.zIndex = "9998"; 

    document.body.appendChild(backgroundBlur); 
    document.body.appendChild(popupContainer);
   // myButton.style.display = "none"; 
    isPopupOpen = true;
  }
}

myButton.addEventListener("click", togglePopup);

document.body.appendChild(myButton);
