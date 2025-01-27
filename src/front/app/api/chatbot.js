import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { message } = await request.json();

  // 간단한 응답 로직
  let response = "I'm not sure how to respond to that.";
  if (message.toLowerCase().includes('hello')) {
    response = "Hello! How can I assist you today?";
  } else if (message.toLowerCase().includes('help')) {
    response = "Sure! Let me know what you need help with.";
  }

  return NextResponse.json({ response });
}