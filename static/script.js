document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/upload-pdf/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('pdfText').value = data.pdf_text;
        } else {
            alert('Failed to upload PDF.');
        }
    }
});

document.getElementById('queryForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const question = document.getElementById('question').value;
    const pdfText = document.getElementById('pdfText').value;
    
    const response = await fetch('/query-pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question, pdf_text: pdfText })
    });
    
    if (response.ok) {
        const data = await response.json();
        document.getElementById('response').innerText = data.response;
    } else {
        alert('Failed to get response.');
    }
});
