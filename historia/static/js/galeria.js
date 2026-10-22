document.querySelectorAll('.galeria-persona').forEach((button) => {
    let photos = Array.from(button.querySelectorAll('img'));
    let current = 0;
    const counter = button.parentElement.querySelector('.contador-fotos');
    const update = () => {
        photos.forEach((photo, index) => { photo.hidden = index !== current; });
        button.disabled = photos.length < 2;
        counter.textContent = photos.length ? `${current + 1} / ${photos.length}` : '';
    };
    photos.forEach((photo) => {
        const removeFailed = () => {
            photos = photos.filter((item) => item !== photo);
            photo.remove();
            current = Math.min(current, Math.max(0, photos.length - 1));
            update();
            if (!photos.length && !button.querySelector('.foto-pendiente')) {
                const placeholder = document.createElement('span');
                placeholder.className = 'foto-pendiente';
                placeholder.textContent = 'Fotografía pendiente';
                button.append(placeholder);
            }
        };
        photo.addEventListener('error', removeFailed, { once: true });
        if (photo.complete && !photo.naturalWidth) removeFailed();
    });
    button.addEventListener('click', () => {
        current = (current + 1) % photos.length;
        update();
    });
    update();
});
