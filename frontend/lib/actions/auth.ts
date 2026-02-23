"use server";

import * as z from "zod";
import { signIn, signOut } from "@/lib/auth";
import { apiFetch } from "@/lib/api";
import { AuthError } from "next-auth";

// ── Validation schemas ────────────────────────────────────────────────

const registerSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(6, "Password must be at least 6 characters")
    .max(128),
});

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

// ── Types ─────────────────────────────────────────────────────────────

export interface AuthResult {
  success: boolean;
  error?: string;
}

// ── Actions ───────────────────────────────────────────────────────────

export async function signUpAction(
  _prev: AuthResult,
  formData: FormData,
): Promise<AuthResult> {
  const raw = {
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const parsed = registerSchema.safeParse(raw);
  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message };
  }

  const { data, error } = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify(parsed.data),
  });

  if (error) {
    return { success: false, error };
  }

  if (!data) {
    return { success: false, error: "Registration failed." };
  }

  return { success: true };
}

export async function signInAction(
  _prev: AuthResult,
  formData: FormData,
): Promise<AuthResult> {
  const raw = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const parsed = loginSchema.safeParse(raw);
  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message };
  }

  try {
    await signIn("credentials", {
      email: parsed.data.email,
      password: parsed.data.password,
      redirect: false,
    });
  } catch (error) {
    if (error instanceof AuthError) {
      return { success: false, error: "Invalid email or password." };
    }
    throw error; // re-throw unexpected errors (e.g. NEXT_REDIRECT)
  }

  return { success: true };
}

export async function googleSignInAction() {
  await signIn("google", { redirectTo: "/dashboard" });
}

export async function signOutAction() {
  await signOut({ redirectTo: "/sign-in" });
}
