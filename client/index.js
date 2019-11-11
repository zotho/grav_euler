import * as THREE from '/node_modules/three/build/three.module.js';
import { ConvexBufferGeometry } from '/lib/ConvexGeometry.js';
import CameraControls from '/node_modules/camera-controls/dist/camera-controls.module.js';
// import { OrbitControls } from './lib/OrbitControls.js';

CameraControls.install( { THREE: THREE } );

import Stats from '/lib/stats.module.js';

let websocket;
let last_rotation_time = 0;

let renderer, scene, camera, clock, controls, stats;
const objects = [];

let WIDTH = window.innerWidth;
let HEIGHT = window.innerHeight;

const init = () => {
    scene = new THREE.Scene();
    clock = new THREE.Clock();

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

    controls = new CameraControls(camera, renderer.domElement);
    controls.addEventListener('controlend', processRotation);
    window.addEventListener('wheel', debounce(processRotation, 500));

    // controls.minDistance = 100;
    // controls.maxDistance = 200;
    // controls.maxPolarAngle = Math.PI / 2;
    // controls.enableZoom = false;
    // controls.enablePan = false;
    // controls.enableRotate = false;

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
    // var time = Date.now() * 0.001;

    const delta = clock.getDelta();
    const updated = controls.update( delta );

    // objects.forEach(object => {
        // object.rotation.x = 0.25 * time;
        // object.rotation.y = 0.25 * time;
    // });

    // camera.rotation.x = time;

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

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
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

const processRotation = () => {
    websocket.send(JSON.stringify({
        action: 'rotate',
        value: controls.toJSON(),
    }));
}

const handleRotation = (stateJSONString, rotation_time) => {
    console.log(stateJSONString);
    if (controls && stateJSONString && rotation_time > last_rotation_time) {
        last_rotation_time = rotation_time
        controls.fromJSON(stateJSONString, true);
    }
}

const initWebSocket = () => {
    const users = document.querySelector('.users');
    // Write your own websocket address. Output of:
    // lt --port 6789
    websocket = new WebSocket("wss://***.localtunnel.me");
    websocket.onmessage = event => {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case 'model':
                buildModel(data.value);
                break;
            case 'rotate':
                handleRotation(data.value, data.rotation_time);
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

initWebSocket();
init();
animate();