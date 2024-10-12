export function active1() {
    return `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
}

export function active2() {
    return `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
}

export function inactive1() {
    return `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
}

export function inactive2() {
    return `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
}
