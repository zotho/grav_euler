import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/109/three.module.js';
import { ConvexBufferGeometry } from '/lib/ConvexGeometry.min.js';
import Stats from '/lib/stats.module.min.js';
import CameraControls from 'https://cdn.jsdelivr.net/npm/camera-controls@1.15.0/dist/camera-controls.module.js';

CameraControls.install( { THREE: THREE } );

let websocket;
let last_rotation_time = 0;

let renderer, scene, camera, clock, controls, stats;
const objects = [];

let WIDTH = window.innerWidth;
let HEIGHT = window.innerHeight;

const init = async () => {
    scene = new THREE.Scene();
    clock = new THREE.Clock();

    renderer = await new THREE.WebGLRenderer({antialias: true});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(WIDTH, HEIGHT);
    var container = await document.getElementById('container');
    await container.appendChild(renderer.domElement);

    camera = await new THREE.PerspectiveCamera(60, WIDTH / HEIGHT, 1, 200);
    camera.position.z = 150;
    scene.background = new THREE.Color(0x111111);
    scene.fog = new THREE.Fog(0x111111, 150, 200);
    // light
    scene.add(new THREE.AmbientLight(0x222222));
    const light = new THREE.PointLight(0xffffff, 1);
    light.position.x = 150;
    camera.add(light);
    scene.add(camera);

    controls = await new CameraControls(camera, renderer.domElement);
    controls.addEventListener('controlend', debounce(processRotation, 100));
    window.addEventListener('wheel', debounce(processRotation, 500));

    stats = new Stats();
    await container.appendChild(stats.dom);

    window.addEventListener('resize', onWindowResize, false);
}

const onWindowResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}

const animate = async () => {
    requestAnimationFrame( animate );

    await render();
    if (stats) {
        await stats.update();
    }
}

const render = async () => {
    const delta = clock.getDelta();
    const updated = controls && controls.update( delta );
    if (renderer) {
        await renderer.render(scene, camera);
    }
}

const buildModel = async data => {
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

    const meshGeometry = await new ConvexBufferGeometry(modelGeometry.vertices);

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

const debounce = (func, wait, immediate) => {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

const processRotation = async () => {
    await websocket.send( await JSON.stringify({
        action: 'rotate',
        value: await controls.toJSON(),
    }));
}

const handleRotation = async (stateJSONString, rotation_time) => {
    if (controls && stateJSONString && rotation_time > last_rotation_time) {
        last_rotation_time = rotation_time
        await controls.fromJSON(stateJSONString, true);
    }
}

const initWebSocket = async () => {
    const users = await document.querySelector('.users');
    // Write your own websocket address. Output of:
    // lt --port 6789
    websocket = await new WebSocket("wss://splendid-warthog-90.localtunnel.me");
    websocket.onmessage = async event => {
        const data = await JSON.parse(event.data);
        switch (data.type) {
            case 'model':
                await buildModel(data.value);
                break;
            case 'rotate':
                await handleRotation(data.value, data.rotation_time);
                break;
            case 'users':
                users.textContent = (
                    await data.count.toString() + " user" + (data.count == 1 ? "" : "s")
                );
                break;
            default:
                console.error(
                    "Unsupported event", data
                );
        }
    };
}

initWebSocket();
init();
animate();