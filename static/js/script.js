document.getElementById('fileInput').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    const fileNameDisplay = document.getElementById('fileName');
    
    if (fileName) {
        fileNameDisplay.textContent = `Selected: ${fileName}`;
        fileNameDisplay.style.color = '#10b981';
    } else {
        fileNameDisplay.textContent = '';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(e) {
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    
    if (fileInput.files.length > 0) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        loading.style.display = 'block';
    }
});