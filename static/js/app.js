document.getElementById('imageForm').onsubmit = async function (event) {
    event.preventDefault();

    const prompt = document.getElementById('prompt').value;
    const model = document.getElementById('model').value;

    const response = await fetch('/generate_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, model })
    });

    const data = await response.json();

    if (data.image_url) {
        document.getElementById('imageResult').innerHTML = `<img src="${data.image_url}" alt="Generated Image">`;
    } else {
        document.getElementById('imageResult').innerHTML = `<p>Error: ${data.error}</p>`;
    }
};
