import * as fs from 'fs';
import * as path from 'path';
import sharp from 'sharp'; // Default import for sharp
import * as chokidar from 'chokidar';

// Directory to watch
const watchDir = path.join(process.env.HOME, 'Pictures/Wallpapers');

const watcher = chokidar.watch(watchDir, {
    persistent: true,
    ignored: /[\/\\]\./,
});

const processImage = async (filePath) => {
    if (path.extname(filePath).toLowerCase() === '.webp') {
        const pngPath = filePath.replace(/\.webp$/, '.png');

        try {
            await sharp(filePath)
                .toFile(pngPath);

            console.log(`Converted: ${filePath} to ${pngPath}`);

            fs.unlinkSync(filePath);
            console.log(`Deleted: ${filePath}`);
        } catch (error) {
            console.error(`Error processing ${filePath}:`, error);
        }
    }
};

watcher.on('add', processImage);
