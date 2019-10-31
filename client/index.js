import * as THREE from '/lib/three.module.js';
import { ConvexBufferGeometry } from '/lib/ConvexGeometry.js';
import { OrbitControls } from './lib/OrbitControls.js';

import Stats from '/lib/stats.module.js';

let renderer, scene, camera, controls, stats;
const objects = [];

let WIDTH = window.innerWidth;
let HEIGHT = window.innerHeight;

const init = () => {
    scene = new THREE.Scene();
    
    renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(WIDTH, HEIGHT);
    var container = document.getElementById('container');
    container.appendChild(renderer.domElement);

    camera = new THREE.PerspectiveCamera(60, WIDTH / HEIGHT, 1, 200);
    camera.position.z = 150;
    scene.background = new THREE.Color(0x111111);
    scene.fog = new THREE.Fog(0x111111, 150, 200);
    // light
    scene.add(new THREE.AmbientLight(0x222222));
    const light = new THREE.PointLight(0xffffff, 1);
    light.position.x = 150;
    camera.add(light);
    scene.add(camera);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.minDistance = 100;
    controls.maxDistance = 200;
    controls.maxPolarAngle = Math.PI / 2;
    // controls.enableZoom = false;
    // controls.enablePan = false;
    // controls.enableRotate = false;
    console.log(controls);

    stats = new Stats();
    container.appendChild(stats.dom);

    window.addEventListener('resize', onWindowResize, false);
}

// const geometryDodecahedron = edge => {
    // 
// }

const onWindowResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}

const animate = () => {
    requestAnimationFrame( animate );

    render();
    stats.update();
}

const render = () => {
    var time = Date.now() * 0.001;

    // objects.forEach(object => {
        // object.rotation.x = 0.25 * time;
        // object.rotation.y = 0.25 * time;
    // });

    camera.rotation.x = time;
    controls.update();

    renderer.render(scene, camera);
}

const buildModel = data => {
    const modelGeometry = new THREE.Geometry();

    for (let coords of data) {
        const point = new THREE.Vector3();
        point.x = coords[0];
        point.y = coords[1];
        point.z = coords[2];

        modelGeometry.vertices.push(point);
    }

    const pointMaterial = new THREE.PointsMaterial({color: 0xffffff});

    const model = new THREE.Points(modelGeometry, pointMaterial);
    scene.add(model);
    objects.push(model);

    var meshMaterial = new THREE.MeshLambertMaterial({
        color: 0xffffff,
        opacity: 0.9,
        transparent: true,
    });

    const meshGeometry = new ConvexBufferGeometry(modelGeometry.vertices);

    let mesh = new THREE.Mesh(meshGeometry, meshMaterial);
    mesh.material.side = THREE.BackSide; // back faces
    mesh.renderOrder = 0;
    scene.add(mesh);
    objects.push(mesh);

    mesh = new THREE.Mesh(meshGeometry, meshMaterial.clone());
    mesh.material.side = THREE.FrontSide; // front faces
    mesh.renderOrder = 1;
    scene.add(mesh);
    objects.push(mesh);
}

const initWebSocket = () => {
    const users = document.querySelector('.users');
    const websocket = new WebSocket("ws://127.0.0.1:6789/");
    websocket.onmessage = event => {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case 'model':
                buildModel(data.value);
                break;
            case 'users':
                users.textContent = (
                    data.count.toString() + " user" + (data.count == 1 ? "" : "s")
                );
                break;
            default:
                console.error(
                    "Unsupported event", data
                );
        }
    };
}

init();
animate();
initWebSocket();