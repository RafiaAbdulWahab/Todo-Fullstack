'use client';
// frontend/src/auth.tsx (formerly frontend/src/lib/auth.ts)
import { Auth } from "better-auth";
import Credentials from "better-auth/credentials";
import fetchWithAuth from './lib/api'; // Import the API client, adjusted path

// Ye hamara authentication ka naya setup hai
export const { auth, handlers, signIn, signOut } = Auth({
  providers: [
    // Pass the Credentials module directly, as instructed
    Credentials,
  ],
  secret: process.env.AUTH_SECRET, // Use environment variable for secret
});

// Custom login function to be used by client components
// Renamed to `authenticate` to avoid conflict with `signIn` from Auth
export async function authenticate(username: string, password: string): Promise<any> {
  // Directly call the signIn function provided by better-auth
  // The 'credentials' provider will handle the authorization logic
  const result = await signIn("credentials", { username, password, redirect: false });

  if (result?.error) {
    throw new Error(result.error);
  }

  return result;
}

interface SignupCredentials {
  name: string;
  email: string;
  password: string;
}

// Custom signup function to be used by client components
export async function signup(credentials: SignupCredentials) {
  try {
    const response = await fetchWithAuth('/register', { // Assuming '/register' is the signup endpoint
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.ok) {
      // If signup is successful, you might want to automatically sign in the user
      // or redirect them to a login page. For now, just return success.
      return { success: true };
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Signup failed');
    }
  } catch (error: any) {
    console.error('Signup API call failed:', error);
    throw error;
  }
}