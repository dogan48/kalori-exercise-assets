# Squat animation — 50-frame specification

Use this prompt with **video generation** (Runway, Kling, Veo, etc.) or a **3D / mocap** pipeline. Frame-by-frame image models cannot reliably satisfy the consistency rules below.

## Master prompt

Create a high-quality, anatomically accurate, seamless 50-frame animation of a woman performing one complete bodyweight squat exercise. The animation will be used in a fitness application to demonstrate the correct exercise technique.

### CRITICAL REQUIREMENT: STRICT FRAME-TO-FRAME CONSISTENCY

The exact same woman must appear in all 50 frames. Maintain identical body proportions, face, hairstyle, clothing, skin tone, lighting, camera angle, perspective, and background throughout the entire sequence.

### 1. FIXED CHARACTER POSITION AND CAMERA

- Use a completely stationary camera and a fixed, unchanging viewpoint.
- Keep the woman's body centered at exactly the same horizontal position in every frame.
- Her feet must remain planted at the same ground coordinates throughout the entire squat.
- Her body must never slide, drift, jump, rotate unexpectedly, or change size between frames.
- Maintain a fixed camera distance, focal length, framing, and perspective.
- Do not change the background, floor, shadows, or lighting.
- The character must remain fully visible, with consistent margins around her body.

### 2. STRICT HAND AND ARM CONSISTENCY

- Both hands must remain anatomically correct, with five naturally formed fingers on each hand.
- Keep both hands open, relaxed, and naturally aligned with the forearms throughout the entire animation.
- The palms and fingers must maintain a consistent, anatomically plausible orientation.
- The fingers must never spontaneously curl into fists, spread unnaturally, disappear, merge, multiply, or change shape.
- No finger snapping, hand twisting, wrist bending, finger deformation, or sudden changes in hand pose.
- Both arms must move smoothly and symmetrically.
- The arms must remain extended forward at approximately shoulder height, with a slight natural bend at the elbows.
- Once the initial arm position is established, preserve the same hand shape and wrist orientation in every subsequent frame.

### 3. CORRECT SQUAT BIOMECHANICS

- Starting position: the woman stands upright, facing the camera at a consistent three-quarter angle, with feet approximately shoulder-width apart and toes pointing slightly outward.
- Her spine remains neutral, chest lifted, and head aligned naturally with the torso.
- During descent, her hips move backward and downward while her knees bend naturally and track in the same direction as her toes.
- Her heels remain firmly on the ground.
- Her arms remain extended forward to help maintain balance.
- At the bottom position, her hips are lowered to a comfortable squat depth, with no exaggerated joint angles or unnatural body deformation.
- During ascent, she smoothly reverses the same movement path and returns to the exact initial standing position.
- Her torso, hips, knees, ankles, shoulders, elbows, wrists, and fingers must move according to realistic human biomechanics.
- No impossible joint rotations, limb stretching, body morphing, or changes in body proportions.

### 4. EXACT 50-FRAME MOTION SEQUENCE

- Frames 1–5: stable upright standing position.
- Frames 6–20: smooth, gradual squat descent.
- Frames 21–25: controlled pause at the bottom of the squat.
- Frames 26–40: smooth, gradual ascent following the reverse of the descent path.
- Frames 41–50: return to the original upright standing position and hold it steadily.

Every consecutive frame must represent a small, natural change from the preceding frame. Motion must be continuous, fluid, and temporally consistent. Avoid sudden pose changes, skipped motion, duplicated poses, or abrupt transitions.

### 5. VISUAL STYLE AND OUTPUT CONSISTENCY

- Use a clean, realistic fitness-instruction visual style.
- Maintain consistent anatomy, clothing, body silhouette, and limb lengths in all frames.
- Keep the entire character within the same fixed image boundaries.
- Do not introduce additional objects, accessories, or visual elements.
- Ensure that the final standing pose matches the initial standing pose as closely as possible, allowing the animation to loop seamlessly.
- Attractive fit woman, age 25–30, athletic build, dark hair in ponytail.
- Gray fitted sports top, black high-waist leggings, white sneakers.
- Soft studio lighting, neutral light gray floor and background (#e8e8e8).
- Full body in frame, vertical 1:1 or 9:16 safe crop with consistent headroom and footroom.
- Photorealistic or high-quality 3D render (not cartoon); no text, logos, or watermarks.
- Output: seamless loop-friendly clip (50 frames at 12–15 fps) or numbered PNG sequence `squat_0001.png` … `squat_0050.png`.

### ABSOLUTE NEGATIVE CONSTRAINTS

No changing character identity, no body position drift, no camera movement, no zooming, no panning, no inconsistent hand shapes, no spontaneous fists, no finger deformation, no extra fingers, no missing fingers, no twisted wrists, no unnatural elbow movement, no asymmetrical arm changes, no floating feet, no foot sliding, no body morphing, no flickering, no sudden jumps, no inconsistent clothing, and no background changes.

### PRIORITY ORDER

1. Preserve character identity and spatial position first.
2. Hand and finger anatomy second.
3. Correct squat biomechanics third.
4. Smooth motion between frames fourth.

Never sacrifice anatomical consistency to create exaggerated movement.

## One-block prompt (paste into video AI)

```
Create a high-quality, anatomically accurate, seamless animation of a woman performing one complete bodyweight squat for a fitness app tutorial. Fixed stationary camera, three-quarter angle, character centered, feet planted same spot, no zoom/pan/drift. Same woman every frame: face, hair, gray top, black leggings, white shoes, light gray studio background. Hands open with five fingers each, arms forward at shoulder height, slight elbow bend—no fists, no finger/wrist deformation, symmetric arms. Neutral spine, hips back on descent, knees track toes, heels down, comfortable depth, smooth ascent to exact start pose for seamless loop. Clean realistic fitness-instruction style; consistent silhouette and limb lengths; fixed frame boundaries; no extra objects. Priority: identity and position, then hands, then biomechanics, then smooth motion. 5s hold stand, gradual descent, brief bottom pause, gradual ascent, hold stand. No morphing, flicker, jumping, clothing or background changes.
```

## Why not frame-by-frame image AI?

Independent image generation per frame breaks temporal consistency (hands, fingers, micro-pose). Blending between keyframes does not fix wrong anatomy in keyframes.

## Recommended production paths

1. **AI video** (single clip): paste master prompt; export MP4; extract 50 frames with ffmpeg.
2. **Mixamo / Blender**: rigged female character + squat animation; render 50 frames.
3. **Stock video**: one continuous take; license OK for app; ffmpeg to GIF.
