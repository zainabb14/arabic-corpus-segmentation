const fileInput = document.getElementById('file-input');
const fileName=document.getElementById('file-name');
const uploadButton=document.getElementById('upload');
const openFileDialogue = () => {
    fileInput.click();
}
fileInput.addEventListener('change', (event) => {
    const name = event.target.value.split('\\').pop() || event.target.files[0].name;
    fileName.style.display="block";
    fileName.textContent = name;
    uploadButton.style.display="block";
});